import tkinter as tk
from tkinter import simpledialog
from tkhtmlview import HTMLLabel
import socket
import threading
from cryptography.fernet import Fernet
import os

client_key_path = "client_encryption_key.key"

def load_client_key():
    if os.path.exists(client_key_path):
        with open(client_key_path, "rb") as key_file:
            return key_file.read()
    return None

def save_client_key(key):
    with open(client_key_path, "wb") as key_file:
        key_file.write(key)

def delete_client_key():
    if os.path.exists(client_key_path):
        os.remove(client_key_path)
        print("Клиентский ключ удален.")

def fetch_key_from_server(client_socket):
    encryption_key = client_socket.recv(1024)
    save_client_key(encryption_key)
    return encryption_key

def encrypt(data, cipher):
    return cipher.encrypt(data)

def decrypt(data, cipher):
    return cipher.decrypt(data)

server_ip = ''

def set_server_ip():
    global server_ip
    server_ip = simpledialog.askstring("Server IP", "Введите IP-адрес сервера:")

def fetch_page(url):
    try:
        port = 8080

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, port))

        # Получаем ключ каждый раз при подключении
        print("Получение ключа от сервера...")
        key = fetch_key_from_server(client_socket)
        print(f"Ключ получен: {key.decode()}")

        cipher = Fernet(key)

        # Формирование и шифрование запроса
        request = f"GET lll://{url} LLL/1.0"
        print(f"Запрос: {request}")
        encrypted_request = encrypt(request.encode('utf-8'), cipher)

        client_socket.sendall(encrypted_request)
        print("Зашифрованный запрос отправлен.")

        # Получение и расшифровка ответа
        encrypted_response = client_socket.recv(4096)
        response = decrypt(encrypted_response, cipher).decode('utf-8')

        client_socket.close()

        headers, html_content = response.split('\n\n', 1)
        print(f"Получен ответ: {headers}")
        return html_content
    except Exception as e:
        error_message = f"Ошибка при получении страницы: {str(e)}"
        print(error_message)
        return f"<html><body><h1>{error_message}</h1></body></html>"

def fetch_and_show_page(url):
    if not server_ip:
        update_html_content("<html><body><h1>IP-адрес сервера не установлен!</h1></body></html>")
    else:
        html_content = fetch_page(url)
        root.after(0, update_html_content, html_content)

def update_html_content(html_content):
    html_label.set_html(html_content)
    root.update_idletasks()
    width = html_label.winfo_reqwidth()
    height = html_label.winfo_reqheight()
    root.geometry(f"{width}x{height}")

def load_page():
    url = url_entry.get()
    threading.Thread(target=fetch_and_show_page, args=(url,)).start()

def on_closing():
    delete_client_key()
    root.destroy()

root = tk.Tk()
root.title("Goat Browser")

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Установить IP сервера", command=set_server_ip)

url_label = tk.Label(root, text="Введите URL:")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

load_button = tk.Button(root, text="Загрузить страницу", command=load_page)
load_button.pack()

html_label = HTMLLabel(root, width=80, height=20)
html_label.pack(fill="both", expand=True)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()