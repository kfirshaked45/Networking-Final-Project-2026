import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 9999

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode('utf-8')
            if not msg:
                print("\n[Disconnected]")
                break

            msg = msg.rstrip() 
            
            print(f"\r{msg}\n> ", end="") 
        except:
            break
    sock.close()
    sys.exit()

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except:
        print("Server not found.")
        return

    try:
        welcome = client.recv(1024).decode('utf-8')
        print(welcome)
        name = input("Name: ")
        client.send(name.encode('utf-8'))
    except:
        return

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()
    
    print("-" * 30)
    print("Chat Started! You are in 'General'.")
    print("To switch room: /join RoomName")
    print("To quit: /exit")
    print("-" * 30)

    try:
        while True:
            msg = input("> ")
            if msg:
                client.send(msg.encode('utf-8'))
    except:
        pass
    finally:
        client.close()

if __name__ == "__main__":
    start_client()