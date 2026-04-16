"""
AES-256-GCM Encrypted UDP Telemetry Client
============================================
Every packet is encrypted with AES-256-GCM before being sent over UDP.
A fresh random 12-byte nonce is generated per packet, so even identical
payloads produce completely different ciphertext each time.

Run:
    python AES_UDP_Client.py
"""

import socket
import json
import time
import random
import os
from Crypto.Cipher import AES

# ─── Shared secret key (must match server) ────────────────────────────────────
AES_KEY = b"ThisIsA32ByteSecretKey4AES256!!!"

# ─── Server address ───────────────────────────────────────────────────────────
SERVER_IP = "192.168.137.1"
PORT      = 9999


def encrypt_packet(payload: dict) -> bytes:
    """
    Encrypts a dict with AES-256-GCM.

    Returns:
        [12 bytes nonce] + [16 bytes GCM tag] + [ciphertext]

    The nonce is randomly generated per packet (never reused).
    The GCM tag allows the server to detect any tampering.
    """
    nonce  = os.urandom(12)                        # cryptographically random
    cipher = AES.new(AES_KEY, AES.MODE_GCM, nonce=nonce)

    plaintext          = json.dumps(payload).encode()
    ciphertext, tag    = cipher.encrypt_and_digest(plaintext)

    return nonce + tag + ciphertext                # fixed-layout packet


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("=" * 55)
    print("  UDP Telemetry Client  (AES-256-GCM Encrypted)")
    print("=" * 55)
    print(f"  Target     : {SERVER_IP}:{PORT}")
    print(f"  Encryption : AES-256-GCM")
    print(f"  Key length : {len(AES_KEY) * 8} bits")
    print(f"\n  Sending encrypted telemetry...\n")

    sequence_number = 0

    while True:
        sequence_number += 1

        telemetry = {
            "seq":          sequence_number,
            "timestamp":    time.time(),
            "cpu_usage":    random.randint(1, 100),
            "memory_usage": random.randint(100, 8000),
        }

        encrypted = encrypt_packet(telemetry)
        sock.sendto(encrypted, (SERVER_IP, PORT))

        print(f"  Sent Packet {sequence_number:>4}  "
              f"cpu={telemetry['cpu_usage']:>3}%  "
              f"mem={telemetry['memory_usage']:>5} MB  "
              f"encrypted_size={len(encrypted)} bytes  [AES-256-GCM ✓]")

        time.sleep(0.1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt: # manually stop the program
        print("\n[Client] Stopped.")
    except ConnectionRefusedError: #not able to connect to the server 
        print("\n[Client] Server not reachable.")