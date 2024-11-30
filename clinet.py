import tkinter as tk
from tkinter import simpledialog
from tkhtmlview import HTMLLabel
import socket
import threading

# глобальная переменная для хранения IP-адреса сервера
server_ip = ''

def set_server_ip():
    global server_ip
    # показываем диалоговое окно для ввода IP-адреса сервера
    server_ip = simpledialog.askstring("Server IP", "Enter Server IP:")

def fetch_page(url):
    try:
        port = 8080

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, port))

        request = f"GET lll://{url} LLL/1.0"
        client_socket.sendall(request.encode('utf-8'))

        response = client_socket.recv(4096).decode('utf-8')
        client_socket.close()

        headers, html_content = response.split('\n\n', 1)
        return html_content
    except Exception as e:
        return f"<html><body><h1>Error fetching page: {str(e)}</h1></body></html>"

def fetch_and_show_page(url):
    if not server_ip:
        update_html_content("<html><body><h1>Server IP not set!</h1></body></html>") # поставь IP сервера балин
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

root = tk.Tk()
root.title("Goat Browser")

# Создаем меню
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Set Server IP", command=set_server_ip)

url_label = tk.Label(root, text="Enter URL:")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

load_button = tk.Button(root, text="Load Page", command=load_page)
load_button.pack()

html_label = HTMLLabel(root, width=80, height=20)
html_label.pack(fill="both", expand=True)

root.mainloop()