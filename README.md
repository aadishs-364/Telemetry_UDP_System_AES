# Telemetry UDP System

A lightweight UDP-based telemetry system for monitoring and collecting real-time system metrics (CPU usage, memory usage) from distributed clients. Built with Python, this system demonstrates client-server communication over UDP with comprehensive analytics and network performance monitoring.

## 📋 Project Overview

This project implements a **distributed telemetry collection system** using UDP (User Datagram Protocol) to efficiently gather system performance data from multiple clients and analyze network reliability metrics in real-time.

**Key Use Cases:**
- Monitor system metrics across distributed devices
- Measure network performance (packet loss, latency, throughput)
- Analyze client-side CPU and memory usage patterns
- Demonstrate UDP communication in Python

## 🏗️ System Architecture

```
┌─────────────────┐         UDP Packets         ┌─────────────────┐
│  UDP Client(s)  │────────────────────────────▶│  UDP Server     │
│ - CPU Usage     │                              │ - Listens on    │
│ - Memory Usage  │ (JSON format, every 100ms)   │   Port 9999     │
│ - Timestamp     │                              │ - Receives Data │
└─────────────────┘                              └────────┬────────┘
                                                          │
                                                          ▼
                                                  ┌──────────────────┐
                                                  │  Analytics Module│
                                                  │ - Packet Stats   │
                                                  │ - Latency Calc   │
                                                  │ - Loss Detection  │
                                                  │ - Stats Report   │
                                                  └──────────────────┘
```

## ✨ Features

- **UDP-based Communication**: Efficient, connectionless protocol for low-latency telemetry
- **Real-time Metrics Collection**: Gathers CPU and memory usage data from clients
- **Network Analytics**:
  - Packet loss detection and calculation
  - Latency measurement (round-trip time)
  - Throughput monitoring (packets/second)
  - Packet loss rate percentage
- **Multi-client Support**: Tracks multiple clients simultaneously with per-client sequence tracking
- **Automatic Statistics**: Prints comprehensive stats every 5 seconds
- **JSON Data Format**: Structured, easy-to-parse telemetry packets

## 📦 Project Structure

```
Telemetry_UDP_System/
├── UDP_Server.py      # Main server that receives and processes telemetry
├── UDP_Client.py      # Client that sends telemetry metrics
├── Analytics.py       # Analytics engine for data processing and reporting
└── README.md          # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher
- No external dependencies (uses only standard library)

### Installation

1. Clone or download the project:
   ```bash
   cd Telemetry_UDP_System
   ```

2. No installation required - all modules use Python standard library

### Running the System

#### 1. Start the Server
Open a terminal and run:
```bash
python UDP_Server.py
```

Expected output:
```
🚀 UDP Telemetry Server Started...
```

#### 2. Start the Client (in another terminal)
```bash
python UDP_Client.py
```

Expected output:
```
Telemetry Client Started...
Sent Packet 1
Sent Packet 2
Sent Packet 3
...
```

#### 3. Monitor the Statistics
The server will automatically print statistics every 5 seconds:
```
------ Telemetry Statistics ------
Packets Received: 50
Packets Lost: 0
Packet Loss Rate: 0.00%
Throughput: 10.00 packets/sec
Average Latency: 0.0012 sec
Active Clients: 1
Average CPU Usage: 45.32%
Average Memory Usage: 2048.50 MB
----------------------------------
```

## 📊 File Descriptions

### UDP_Server.py
**Purpose**: Main server component that listens for incoming UDP packets and processes telemetry data.

**Key Components**:
- **Socket Configuration**: Binds to `0.0.0.0:9999` to accept connections on all interfaces
- **Packet Reception**: Listens for JSON-encoded telemetry packets
- **Analytics Integration**: Forwards packets to Analytics module for processing
- **Statistics Output**: Prints aggregated metrics every 5 seconds

**Data Flow**:
1. Receives UDP packet (1024 bytes max)
2. Decodes JSON data
3. Extracts client address and packet contents
4. Passes to Analytics for processing

### UDP_Client.py
**Purpose**: Client application that generates and transmits system telemetry data to the server.

**Key Components**:
- **Telemetry Generation**: Creates packets with:
  - `seq`: Sequence number for packet tracking
  - `timestamp`: Client-side generation timestamp
  - `cpu_usage`: Simulated CPU usage (1-100%)
  - `memory_usage`: Simulated memory usage (100-8000 MB)
- **Transmission Rate**: Sends packets every 100ms (~10 packets/sec)
- **Server Configuration**: Connects to `127.0.0.1:9999`

**Packet Format**:
```json
{
  "seq": 1,
  "timestamp": 1712000000.123456,
  "cpu_usage": 45,
  "memory_usage": 2048
}
```

### Analytics.py
**Purpose**: Core analytics engine that processes packets and calculates network/system metrics.

**Key Metrics Calculated**:

1. **Packet Loss Detection**
   - Tracks expected sequence numbers per client
   - Detects gaps in sequence
   - Calculates loss rate: `(lost_packets / total_packets) * 100`

2. **Latency Calculation**
   - Measures time between client timestamp and server reception
   - Formula: `latency = server_time - client_timestamp`
   - Averages all latencies

3. **Throughput Measurement**
   - Packets received per second: `received_packets / elapsed_time`

4. **Resource Monitoring**
   - Average CPU usage across all packets
   - Average memory usage across all packets
   - Tracks active/connected clients

5. **Statistics Reset**
   - Resets counters every reporting interval
   - Maintains continuous sliding-window analytics

**Key Methods**:
- `process_packet(packet, addr)`: Processes incoming telemetry
- `print_stats()`: Generates and displays statistics report
- `reset()`: Resets counters for next reporting interval

## 🔧 Configuration

### Server Configuration (UDP_Server.py)
```python
HOST = "0.0.0.0"      # Listen on all interfaces
PORT = 9999            # UDP port number
```

### Client Configuration (UDP_Client.py)
```python
SERVER_IP = "127.0.0.1"    # Server address
SERVER_PORT = 9999         # Server port
```

### Metrics Reporting Interval (UDP_Server.py)
```python
if time.time() - last_print > 5:    # Reports every 5 seconds
```

## 📈 Understanding the Statistics

| Metric | Description | Unit |
|--------|-------------|------|
| **Packets Received** | Total packets successfully delivered | count |
| **Packets Lost** | Detected missing packets (gaps in sequence) | count |
| **Packet Loss Rate** | Percentage of lost packets | % |
| **Throughput** | Successful delivery rate | packets/sec |
| **Average Latency** | Mean network delay from client to server | seconds |
| **Active Clients** | Number of unique connected clients | count |
| **Average CPU Usage** | Mean CPU usage across all packets | % |
| **Average Memory Usage** | Mean memory usage across all packets | MB |

## 🧪 Testing & Modifications

### Multi-Client Simulation
Start multiple client instances in separate terminals:
```bash
# Terminal 2
python UDP_Client.py

# Terminal 3
python UDP_Client.py

# Terminal 4
python UDP_Client.py
```

The server automatically tracks each client separately by IP:Port and maintains independent sequence numbers.

### Adjusting Metrics
- **Send Frequency**: Change `time.sleep(0.1)` in UDP_Client.py (lower = higher throughput)
- **Reporting Interval**: Change `if time.time() - last_print > 5:` value in UDP_Server.py
- **Server Port**: Modify `PORT = 9999` in both files
- **Packet Size**: Change `sock.recvfrom(1024)` buffer size

### Testing Packet Loss
Simulate packet loss by:
1. Introducing network latency (Windows: `netsh interface tcp set global autotuninglevel=disabled`)
2. Using network simulation tools (NetLimiter, TMeter)
3. Adding artificial delays in client transmission

## ⚠️ Limitations & Considerations

1. **UDP Characteristics**:
   - No guaranteed delivery (packets may be lost)
   - No acknowledgments
   - Out-of-order delivery possible
   - No connection state

2. **Current Implementation**:
   - Simulated metrics (not actual system metrics)
   - Single server instance (not load-balanced)
   - In-memory data (no persistence)
   - Statistics reset periodically

3. **Scalability**:
   - No database integration
   - No distributed storage
   - Memory consumption grows with active clients

## 🔄 Future Enhancements

- [ ] Replace simulated metrics with actual `psutil` calls
- [ ] Add database persistence (MongoDB, PostgreSQL)
- [ ] Implement web dashboard for real-time visualization
- [ ] Add authentication and encryption
- [ ] Deploy with multiple server instances behind load balancer
- [ ] Add configurable filtering and alerts
- [ ] Implement time-series data aggregation

## 📝 Educational Context

This project is part of **Computer Networks Course (SEM 4)** at PES College, demonstrating:
- UDP protocol fundamentals
- Client-server architecture
- Network reliability metrics
- Real-time data processing
- JSON serialization
- Socket programming in Python

## 📄 License

Educational project - Use for learning purposes.

## 👨‍💻 Author

Created for Computer Networks Lab - PES College

---

**Notes**: For production use, consider upgrading to TCP, adding data persistence, implementing proper error handling, and securing the communication channel.
