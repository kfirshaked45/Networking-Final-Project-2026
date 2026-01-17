import socket

# הגדרות הזהות של השרת - מותאם ל-CSV ול-PCAP
HOST = '127.0.0.1'  # כתובת מקומית
PORT = 8080        # הפורט המדויק שמופיע בלכידה וב-CSV המתוקן

def run_server():
    # יצירת Socket מסוג TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # פתרון לבעיית "Address already in use"
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"*** Server is listening on {HOST}:{PORT} ***")
        print("Waiting for messages matching the CSV scenarios...")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                data = conn.recv(1024)
                if not data:
                    continue
                
                received_message = data.decode('utf-8')
                print(f"\n[SERVER] Received Request from {addr}:")
                print(f"---")
                print(received_message.strip())
                print(f"---")

                # תרחיש 1: בדיקת תור (GET /job/queue)
                if "GET /job/queue" in received_message:
                    response = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: application/json\r\n"
                        "Content-Length: 45\r\n"
                        "\r\n"
                        '{"status":"success","queue_size":5}'
                    )
                    print("[SERVER] Matching CSV Row 1-2: Sending 200 OK (JSON Data)")

                # תרחיש 2: שליחת עבודה (POST /job/submit)
                elif "POST /job/submit" in received_message:
                    response = (
                        "HTTP/1.1 302 Found\r\n"
                        "Location: /job/status/101\r\n"
                        "Content-Length: 0\r\n"
                        "\r\n"
                    )
                    print("[SERVER] Matching CSV Row 3-4: Sending 302 Found (Redirect)")
                
                # תרחיש ברירת מחדל
                else:
                    response = "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n"
                    print("[SERVER] Path not in CSV. Sending 404.")

                conn.sendall(response.encode('utf-8'))

    except KeyboardInterrupt:
        print("\nServer shutting down.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    run_server()