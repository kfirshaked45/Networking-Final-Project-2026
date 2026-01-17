🌐 Networking Final Project - 2026
Authors: Kfir Shaked, Noam Bitton, Eyal Raveh
This repository contains the final project for the Computer Networking course. The project is divided into two main parts: Encapsulation & Packet Analysis and a Multi-user Chat System.

📋 Project Overview
Part 1: Encapsulation & Packet Capture
In this section, we simulated a standard HTTP communication (GET/POST) between a client and a server.

Application Layer: Defined custom HTTP messages in a .csv file.

Encapsulation Process: Developed a Python script to wrap application data into TCP segments and IP packets.

Analysis: Captured the local traffic using Wireshark to analyze the headers and verify the data flow through the network layers.

Part 2: Multi-threaded Chat System
A robust, real-time chat application based on the TCP protocol, supporting multiple concurrent users.

Multi-threading: Handles 5+ clients simultaneously without blocking.

Chat Rooms: Users can join specific rooms using the /join command.

Private Messaging: Supports "Whispering" (/w [name] [message]) to ensure private communication that other users cannot see.

Error Handling: Built-in protection against unexpected disconnections and duplicate usernames.

🛠 Tech Stack
Language: Python 3.x

Libraries: socket, threading, sys

Tools: Wireshark (Traffic Analysis)

📂 Project Structure
Plaintext

├── Part1_Encapsulation/
│ ├── server_http.py # HTTP Server simulation
│ ├── client_http.py # HTTP Client (reads from CSV)
│ ├── group0_http_input.csv # Application layer data
│ └── report_capture.pcap # Captured traffic file
├── Part2_Chat_System/
│ ├── chat_server.py # Multi-threaded server
│ └── chat_client.py # Chat client interface
├── Docs/
│ └── Final_Report.pdf # Detailed project documentation
└── README.md
🚀 Getting Started
Running the HTTP Simulation (Part 1)
Start the server:

Bash

python Part1_Encapsulation/server_http.py
Run the client to send messages from the CSV:

Bash

python Part1_Encapsulation/client_http.py
Running the Chat System (Part 2)
Start the Server:

Bash

python Part2_Chat_System/chat_server.py
Connect Clients: Open multiple terminals (up to 5) and run:

Bash

python Part2_Chat_System/chat_client.py
In-Chat Commands:

/join [RoomName] - Switch chat rooms.

/w [Username] [Message] - Send a private message.

/exit - Disconnect safely.

🔍 Wireshark Analysis
During the project, we analyzed the following:

TCP Three-Way Handshake: (SYN -> SYN-ACK -> ACK).

Encapsulation: Verifying the data payload is correctly nested within the TCP and IP headers.

Protocol Verification: Ensuring HTTP methods and custom chat commands are transmitted correctly as cleartext over the socket.
