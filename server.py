import socket
import threading
import os

# Директория, где находятся сайты
SITES_DIR = 'sites'

def handle_client(client_socket):
    try:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break

            print(f"Received request: {request}")

            if request.startswith('GET'):
                parts = request.split()
                if len(parts) >= 2:
                    url = parts[1]
                    if url.startswith('lll://'):
                        domain = url[6:]
                        file_path = os.path.join(SITES_DIR, domain)

                        if os.path.isfile(file_path):
                            with open(file_path, 'r', encoding='utf-8') as file:
                                response_content = file.read()
                            response = f"LLL/1.0 200 OK\n\n{response_content}"
                        else:
                            response = "LLL/1.0 404 Not Found\n\n404 File Not Found"
                    else:
                        response = "LLL/1.0 400 Bad Request\n\n400 Bad Request"
                else:
                    response = "LLL/1.0 400 Bad Request\n\n400 Bad Request"

            client_socket.sendall(response.encode('utf-8'))

    finally:
        client_socket.close()

def lll_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"LLL server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    # Убедитесь, что папка "sites" существует
    os.makedirs(SITES_DIR, exist_ok=True)

    lll_server('localhost', 8080)  # Используем порт 8080