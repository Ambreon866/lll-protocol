import os
import socket
import threading
from cryptography.fernet import Fernet
import mimetypes

# Директория, где находятся сайты
SITES_DIR = 'sites'

# Генерация или загрузка ключа шифрования
def load_or_generate_key():
    key_path = "encryption_key.key"
    if os.path.exists(key_path):
        with open(key_path, "rb") as key_file:
            key = key_file.read()
    else:
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
    return key

encryption_key = load_or_generate_key()
cipher = Fernet(encryption_key)

def encrypt(data):
    return cipher.encrypt(data)

def decrypt(data):
    return cipher.decrypt(data)

def get_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or 'application/octet-stream'

def handle_client(client_socket):
    try:
        # Отправка клиенту ключа шифрования
        client_socket.sendall(encryption_key)
        print(f"Ключ отправлен клиенту")

        while True:
            encrypted_request = client_socket.recv(4096)
            if not encrypted_request:
                break

            try:
                request = decrypt(encrypted_request).decode('utf-8')
                print(f"Получен запрос: {request}")
            except Exception as e:
                print(f"Ошибка расшифровки: {str(e)}")
                break

            if request.startswith('GET'):
                parts = request.split()
                if len(parts) >= 2:
                    url = parts[1]
                    if url.startswith('lll://'):
                        domain = url[6:]
                        file_path = os.path.join(SITES_DIR, domain, "index.html")

                        if os.path.isfile(file_path):
                            mime_type = get_mime_type(file_path)
                            with open(file_path, 'rb') as file:
                                response_content = file.read()
                            response = f"LLL/1.0 200 OK\nContent-Type: {mime_type}\n\n".encode() + response_content
                        else:
                            response_content = "404 File Not Found".encode()
                            response = f"LLL/1.0 404 Not Found\nContent-Type: text/plain\n\n".encode() + response_content
                    else:
                        response_content = "400 Bad Request".encode()
                        response = f"LLL/1.0 400 Bad Request\nContent-Type: text/plain\n\n".encode() + response_content
                else:
                    response_content = "400 Bad Request".encode()
                    response = f"LLL/1.0 400 Bad Request\nContent-Type: text/plain\n\n".encode() + response_content

            encrypted_response = encrypt(response)
            client_socket.sendall(encrypted_response)
            print("Ответ отправлен клиенту")
    
    finally:
        print("Соединение закрыто")
        client_socket.close()

def ensure_site_directories():
    # Получаем список всех подкаталогов в SITES_DIR
    for domain in os.listdir(SITES_DIR):
        domain_dir = os.path.join(SITES_DIR, domain)
        if os.path.isdir(domain_dir):  # Проверяем, что это действительно каталог
            index_file = os.path.join(domain_dir, "index.html")
            if not os.path.isfile(index_file):
                with open(index_file, 'w') as f:
                    f.write(f"<html><body><h1>Welcome to {domain}</h1></body></html>")
                print(f"Создан {index_file} для домена {domain}")

def lll_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"LLL сервер слушает на {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Соединение принято от {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    os.makedirs(SITES_DIR, exist_ok=True)
    ensure_site_directories()
    lll_server('localhost', 8080)
