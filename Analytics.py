import time
from collections import defaultdict

class Analytics:
    def __init__(self):
        self.start_time = time.time()

        self.received_packets = 0
        self.lost_packets = 0
        self.expected_seq = {}  # per client sequence tracking

        self.total_latency = 0
        self.latency_count = 0

        self.clients = set()

        self.cpu_values = []
        self.memory_values = []

    def process_packet(self, packet, addr):
        current_time = time.time()

        seq = packet.get("seq")
        timestamp = packet.get("timestamp")
        cpu = packet.get("cpu_usage")
        memory = packet.get("memory_usage")

        client_id = addr  # (IP, port)

        # Track active clients
        self.clients.add(client_id)

        # Packet count
        self.received_packets += 1

        # Sequence tracking per client
        if client_id not in self.expected_seq:
            self.expected_seq[client_id] = seq
        else:
            expected = self.expected_seq[client_id]
            if seq > expected:
                self.lost_packets += (seq - expected)
            self.expected_seq[client_id] = seq + 1

        # Latency calculation
        if timestamp:
            latency = current_time - timestamp
            self.total_latency += latency
            self.latency_count += 1

        # Store telemetry values
        if cpu is not None:
            self.cpu_values.append(cpu)

        if memory is not None:
            self.memory_values.append(memory)

    def print_stats(self):
        elapsed = time.time() - self.start_time

        if elapsed == 0:
            return

        throughput = self.received_packets / elapsed

        total_packets = self.received_packets + self.lost_packets

        loss_rate = (self.lost_packets / total_packets * 100) if total_packets > 0 else 0

        avg_latency = (self.total_latency / self.latency_count) if self.latency_count > 0 else 0

        avg_cpu = sum(self.cpu_values) / len(self.cpu_values) if self.cpu_values else 0
        avg_memory = sum(self.memory_values) / len(self.memory_values) if self.memory_values else 0

        print("\n------ Telemetry Statistics ------")
        print(f"Packets Received: {self.received_packets}")
        print(f"Packets Lost: {self.lost_packets}")
        print(f"Packet Loss Rate: {loss_rate:.2f}%")
        print(f"Throughput: {throughput:.2f} packets/sec")
        print(f"Average Latency: {avg_latency:.4f} sec")
        print(f"Active Clients: {len(self.clients)}")
        print(f"Average CPU Usage: {avg_cpu:.2f}%")
        print(f"Average Memory Usage: {avg_memory:.2f} MB")
        print("----------------------------------\n")

        # Reset stats every interval (optional)
        self.reset()

    def reset(self):
        self.start_time = time.time()
        self.received_packets = 0
        self.lost_packets = 0
        self.total_latency = 0
        self.latency_count = 0
        self.cpu_values = []
        self.memory_values = []
        

