"""
AES-256-GCM Encrypted UDP Telemetry Server
============================================
AES-256-GCM provides:
  - Confidentiality  : data is encrypted (no one can read it in transit)
  - Integrity        : GCM tag detects any tampering
  - Authenticity     : shared key proves sender identity

Run:
    python AES_UDP_Server.py
"""

import socket
import json
import time
import threading
from Crypto.Cipher import AES
from Analytics import Analytics

# ─── Shared secret key (must match client) ────────────────────────────────────
# 32 bytes = AES-256.  In production, exchange this via a key-agreement
# protocol (e.g. Diffie-Hellman).  For this demo a pre-shared key is used.
AES_KEY = b"ThisIsA32ByteSecretKey4AES256!!!"

# ─── Server config ────────────────────────────────────────────────────────────
HOST = "0.0.0.0"
PORT = 9999

analytics      = Analytics()
analytics_lock = threading.Lock()


def decrypt_packet(raw_bytes: bytes) -> dict | None:
    """
    Packet layout (all lengths fixed):
        [12 bytes nonce] [16 bytes GCM tag] [N bytes ciphertext]

    Returns the decoded dict, or None if decryption/auth fails.
    """
    try:
        if len(raw_bytes) < 28:          # 12 + 16 minimum
            return None

        nonce      = raw_bytes[:12]
        tag        = raw_bytes[12:28]
        ciphertext = raw_bytes[28:]

        cipher    = AES.new(AES_KEY, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)   # raises if tampered

        return json.loads(plaintext.decode())

    except (ValueError, KeyError):
        # GCM authentication failed — packet was tampered or key is wrong
        return None
    except Exception as e:
        print(f"  [!] Decrypt error: {e}")
        return None


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))

    print("=" * 55)
    print("  UDP Telemetry Server  (AES-256-GCM Encrypted)")
    print("=" * 55)
    print(f"  Listening on UDP {HOST}:{PORT}")
    print(f"  Encryption : AES-256-GCM")
    print(f"  Key length : {len(AES_KEY) * 8} bits\n")

    last_print = time.time()

    while True:
        try:
            raw_data, addr = sock.recvfrom(65535)

            packet = decrypt_packet(raw_data)

            if packet is None:
                print(f"  [!] REJECTED packet from {addr} — auth failed or tampered!")
                continue

            with analytics_lock:
                analytics.process_packet(packet, addr)

            print(f"  [+] {addr}  seq={packet.get('seq')}  "
                  f"cpu={packet.get('cpu_usage')}%  "
                  f"mem={packet.get('memory_usage')} MB  "
                  f"[AES-256-GCM ✓]")

            if time.time() - last_print > 5:
                with analytics_lock:
                    analytics.print_stats()
                last_print = time.time()

        except KeyboardInterrupt:
            print("\n[Server] Shutting down.")
            break
        except Exception as e:
            print(f"[Server] Error: {e}")


if __name__ == "__main__":
    main()