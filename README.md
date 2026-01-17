# 🌐 Networking Final Project - 2026
### Authors: Kfir Shaked • Noam Bitton • Eyal Raveh

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![TCP/IP](https://img.shields.io/badge/Protocol-TCP%2FIP-orange?style=for-the-badge)
![Wireshark](https://img.shields.io/badge/Analysis-Wireshark-blue?style=for-the-badge)

---

## 📖 Overview
This repository contains our final project for the Computer Networking course. We focused on two core areas: **Protocol Encapsulation** and **Real-time Communication** using Python Sockets.

---

## 🔬 Part 1: Encapsulation & Packet Analysis
In this section, we simulated how data travels from the Application layer down to the Network layer.

* **Application Data:** Custom HTTP GET/POST requests stored in `group0_http_input.csv`.
* **Encapsulation Logic:** A Python engine that wraps raw data into valid TCP segments and IP packets.
* **Verification:** Full traffic analysis using Wireshark to confirm header integrity.



---

## 💬 Part 2: Multi-threaded Chat System
A robust chat server designed to handle multiple concurrent clients with low latency.

### Core Features:
* **Multi-threading:** Supports 5+ simultaneous connections using the `threading` library.
* **Private Messaging (Whisper):** Send secure messages using `/w [username] [msg]`.
* **Room Management:** Dynamic switching between channels with `/join [RoomName]`.
* **Safety:** Built-in protection against duplicate usernames and sudden client disconnections.

---

## 📂 Project Structure
```text
├── Part1_Encapsulation/
│   ├── server_http.py          # HTTP Server simulation
│   ├── client_http.py          # HTTP Client (CSV Reader)
│   ├── group0_http_input.csv   # Mock Application Data
│   └── report_capture.pcap     # Wireshark Capture
├── Part2_Chat_System/
│   ├── chat_server.py          # Multi-threaded TCP Server
│   └── chat_client.py          # Terminal-based Client
└── README.md
