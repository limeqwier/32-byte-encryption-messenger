import socket
import threading
from cryptography.fernet import Fernet
import random

HOST = 'YOUR_IP'
PORT = random.randint(1024, 65535)  # генерируем случайный порт
BACKLOG = 10
KEY = b'3ifz_EJdHWdyUhRlJ_wGl6UHm_Oc28PRgUxW19R8bZk=' # 32-байтовый ключ шифрования

def handle_client(client_socket, address, clients):
    print(f'New connection from {address}')
    clients.append(client_socket)
    while True:
        try:
            # Получаем зашифрованное сообщение от клиента
            data = client_socket.recv(1024)
            if not data:
                break
            # Расшифровываем сообщение
            f = Fernet(KEY)
            message = f.decrypt(data)
            # Отправляем расшифрованное сообщение всем клиентам, кроме отправителя
            for client in clients:
                if client != client_socket:
                    # Шифруем сообщение для каждого клиента
                    encrypted_message = f.encrypt(message)
                    client.send(encrypted_message)
        except Exception as e:
            print(f'Error handling client {address}: {e}')
            break
    clients.remove(client_socket)
    client_socket.close()
    print(f'Connection closed from {address}')

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(BACKLOG)
    clients = []
    print(f'Server started on {HOST}:{PORT}')
    while True:
        client_socket, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address, clients))
        client_thread.start()

if __name__ == '__main__':
    main()
