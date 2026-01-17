import pandas as pd
import time
import socket
SERVER_HOST = '127.0.0.1' 
SERVER_PORT = 8080
IP_MAPPING = {
    'web_server': (SERVER_HOST, SERVER_PORT),
    'client_browser': (SERVER_HOST, 0)
}
file_path = 'group02_http_input.csv'

def readFile(path):
    try:
        df = pd.read_csv(path)
        print("Server file has loaded")
        print(df.head())
    except FileNotFoundError:
        print(f"File not found {path}")
    msgs = saveMessages(df)
    return msgs

def saveMessages(file):
    MESSAGES_TO_SEND = []
    for index, row in file.iterrows():
        
        src_app = row['src_app']
        dst_app = row['dst_app']

        http_message = row['message']
        
        MESSAGES_TO_SEND.append({
            'src': src_app,
            'dst': dst_app,
            'http_data': http_message
        })
    return MESSAGES_TO_SEND

def runSimulation(messages):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(IP_MAPPING['web_server']) # הלקוח מתחבר לשרת
        for msg in messages:
            # רק בקשות מהלקוח (GET, POST) יישלחו על ידי סוקט זה
            if msg['src'] == 'client_browser':
                print(f"[{msg['src']} -> {msg['dst']}]: Sending {msg['http_data'][:25]}...")
                
                # המרת המחרוזת לבתים (bytes) לפני שליחה
                data_to_send = msg['http_data'].encode('utf-8')
                client_socket.sendall(data_to_send)
                time.sleep(0.5)  
    except ConnectionRefusedError:
        print("\nFATAL ERROR: Connection refused. Ensure your server is running and listening on port 8080.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        print("Socket closed.")      

messages_list = readFile(file_path)

if messages_list:
    runSimulation(messages_list)