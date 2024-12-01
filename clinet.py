import sys
import socket
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLineEdit, QPushButton, 
                             QVBoxLayout, QWidget, QMenuBar, QAction, QInputDialog)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QThread, pyqtSignal
from cryptography.fernet import Fernet

class NetworkThread(QThread):
    response_received = pyqtSignal(str)

    def __init__(self, server_ip, server_port, url):
        super().__init__()
        self.server_ip = server_ip
        self.server_port = server_port
        self.url = url

    def run(self):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.server_ip, self.server_port))
            
            # Получаем ключ шифрования от сервера
            encryption_key = client_socket.recv(4096)
            cipher = Fernet(encryption_key)
            
            # Шифрование и отправка запроса
            encrypted_request = cipher.encrypt(f"GET {self.url}".encode('utf-8'))
            client_socket.sendall(encrypted_request)
            
            # Получение и дешифровка ответа
            encrypted_response = client_socket.recv(4096)
            decrypted_response = cipher.decrypt(encrypted_response).decode('utf-8')

            # Отделяем заголовки от содержимого
            headers, _, content = decrypted_response.partition('\n\n')
            
            self.response_received.emit(content)
        
        except Exception as e:
            error_message = f"<html><body><h1>Ошибка подключения</h1><p>{str(e)}</p></body></html>"
            self.response_received.emit(error_message)
        
        finally:
            client_socket.close()

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Goat Browser")
        self.setMinimumSize(800, 600)
        
        # Используем базовый IP и порт
        self.server_ip = "localhost"
        self.server_port = 8080

        self.browser = QWebEngineView()
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Введите lll:// URL")

        self.go_button = QPushButton("Перейти")
        self.go_button.clicked.connect(self.load_url)

        layout = QVBoxLayout()
        layout.addWidget(self.url_input)
        layout.addWidget(self.go_button)
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.create_menu()

    def create_menu(self):
        menubar = self.menuBar()

        server_menu = menubar.addMenu("Меню")
        
        set_server_action = QAction("Сервер", self)
        set_server_action.triggered.connect(self.set_server)
        
        set_port_action = QAction("Порт", self)
        set_port_action.triggered.connect(self.set_port)

        server_menu.addAction(set_server_action)
        server_menu.addAction(set_port_action)

    def set_server(self):
        server_ip, ok = QInputDialog.getText(self, "Сервер", "Введите адрес сервера:")
        if ok and server_ip:
            self.server_ip = server_ip

    def set_port(self):
        port, ok = QInputDialog.getInt(
            self, "Порт", "Введите порт сервера:", value=self.server_port, min=1, max=65535)
        if ok:
            self.server_port = port

    def load_url(self):
        url = self.url_input.text()
        
        self.network_thread = NetworkThread(self.server_ip, self.server_port, url)
        self.network_thread.response_received.connect(self.display_response)
        self.network_thread.start()

    def display_response(self, content):
        self.browser.setHtml(content)
        self.adjust_window_size()

    def adjust_window_size(self):
        # Используйте JavaScript для получения высоты содержимого и адаптации окна
        self.browser.page().runJavaScript(
            "document.documentElement.scrollHeight", self.on_window_size_calculated)

    def on_window_size_calculated(self, height):
        # Если высота страницы больше текущей высоты окна, измените размер окна
        if height > self.height():
            new_size = self.size()
            new_size.setHeight(height + 50)  # немного добавим для отступа
            self.resize(new_size)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())
