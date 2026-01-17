import socket
import threading

HOST = '127.0.0.1'
PORT = 9999

class Colors:
    PURPLE = '\033[95m' 
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'   
    BOLD = '\033[1m'

rooms = {
    'General': [],
    'Sports': [],
    'Dev': []
}

clients = {}

def check_name_exists(name):
    for user_data in clients.values():
        if user_data['name'] == name:
            return True
    return False

def broadcast(message, room_name, sender_socket=None):
    for client in rooms[room_name][:]:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                remove_client(client)

def send_private_message(sender_socket, target_name, message):
    sender_name = clients[sender_socket]['name']
    target_socket = None

    for sock, info in clients.items():
        if info['name'] == target_name:
            target_socket = sock
            break

    if target_socket:
        try:

            incoming_whisper = f"{Colors.PURPLE} [Whisper from {sender_name}]: {message}{Colors.RESET}"
            target_socket.send(incoming_whisper.encode('utf-8'))
            
            outgoing_confirmation = f"{Colors.PURPLE} [Whisper to {target_name}]: {message}{Colors.RESET}"
            sender_socket.send(outgoing_confirmation.encode('utf-8'))
        except:
            sender_socket.send(f"{Colors.RED}System: Failed to send message to {target_name}.{Colors.RESET}".encode('utf-8'))
    else:
        sender_socket.send(f"{Colors.RED}System: User '{target_name}' not found.{Colors.RESET}".encode('utf-8'))

def remove_client(client_socket):
    if client_socket in clients:
        try:
            user_data = clients[client_socket]
            room = user_data['room']
            name = user_data['name']
            
            if client_socket in rooms[room]:
                rooms[room].remove(client_socket)
            
            del clients[client_socket]
            
            print(f"[DISCONNECT] {name} disconnected.")
            broadcast(f"{Colors.GREEN}[System] {name} left the chat.{Colors.RESET}", room)
        except:
            pass

def handle_client(client_socket, client_address):
    name = ""
    try:
        client_socket.send("Welcome! Enter your name:".encode('utf-8'))
        name = client_socket.recv(1024).decode('utf-8').strip()
        
        if check_name_exists(name):
            error_msg = f"Error: The name '{name}' is already taken. Please reconnect with a different name."
            client_socket.send(error_msg.encode('utf-8'))
            print(f"[REJECT] Connection from {client_address} rejected (Name '{name}' taken).")
            client_socket.close()
            return

        current_room = 'General'
        rooms[current_room].append(client_socket)
        clients[client_socket] = {'name': name, 'room': current_room}
        
        print(f"[NEW] {name} connected from {client_address}")
        
        welcome_msg = (f"{Colors.CYAN}Connected to '{current_room}' successfully!\n"
                       f"Commands: /join [RoomName], /w [Name] [Msg], /exit{Colors.RESET}\n")
        client_socket.send(welcome_msg.encode('utf-8'))
        
        broadcast(f"{Colors.GREEN}[System] {name} joined the room.{Colors.RESET}", current_room, client_socket)

        while True:
            try:
                msg = client_socket.recv(1024).decode('utf-8')
                if not msg:
                    break
                
                if msg.startswith('/'):
                    if msg.startswith('/w ') or msg.startswith('/whisper '):
                        parts = msg.split(' ', 2) 
                        if len(parts) >= 3:
                            target_user = parts[1]
                            private_content = parts[2]
                            send_private_message(client_socket, target_user, private_content)
                        else:
                            client_socket.send("Usage: /w [Name] [Message]".encode('utf-8'))
                    
                    elif msg.startswith('/join'):
                        parts = msg.split(' ')
                        if len(parts) > 1:
                            new_room = parts[1]
                            if new_room not in rooms:
                                rooms[new_room] = []
                            
                            rooms[current_room].remove(client_socket)
                            broadcast(f"{Colors.GREEN}[System] {name} moved to {new_room}.{Colors.RESET}", current_room)
                            
                            current_room = new_room
                            rooms[current_room].append(client_socket)
                            clients[client_socket]['room'] = current_room
                            
                            client_socket.send(f"{Colors.CYAN}Joined room: {current_room}{Colors.RESET}".encode('utf-8'))
                            broadcast(f"{Colors.GREEN}[System] {name} joined the room.{Colors.RESET}", current_room, client_socket)
                        else:
                            client_socket.send("Usage: /join RoomName".encode('utf-8'))
                    
                    elif msg == '/exit':
                        break
                
                else:
                    formatted_msg = f"{name}: {msg}"
                    print(f"[{current_room}] {formatted_msg}")
                    broadcast(formatted_msg, current_room, client_socket)

            except ConnectionResetError:
                break
            except Exception as e:
                break

    except Exception:
        pass
    finally:
        remove_client(client_socket)
        try:
            client_socket.close()
        except:
            pass

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST, PORT))
        server.listen()
        print(f"*** Final Chat Server Running on {HOST}:{PORT} ***")
        
        while True:
            client, addr = server.accept()
            threading.Thread(target=handle_client, args=(client, addr)).start()
    except Exception as e:
        print(f"Server error: {e}")

if __name__ == "__main__":
    start_server()