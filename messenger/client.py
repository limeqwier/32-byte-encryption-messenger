import socket
import threading
from cryptography.fernet import Fernet

SERVER_HOST = 'YOUR_IP'
KEY = b'3ifz_EJdHWdyUhRlJ_wGl6UHm_Oc28PRgUxW19R8bZk=' # 32-байтовый ключ шифрования

def send_message(sock, message):
    # Шифруем сообщение перед отправкой
    f = Fernet(KEY)
    encrypted_message = f.encrypt(message.encode())
    sock.send(encrypted_message)

def receive_message(sock):
    # Получаем зашифрованное сообщение от сервера
    data = sock.recv(1024)
    # Расшифровываем сообщение
    f = Fernet(KEY)
    message = f.decrypt(data).decode()
    return message

def handle_server_messages(sock):
    while True:
        try:
            # Принимаем сообщение от сервера
            received_message = receive_message(sock)
            print(f'Received: {received_message}')
        except socket.error:
            # Сокет закрыт, выходим из цикла
            break

def handle_user_input(sock):
    while True:
        # Получаем сообщение от пользователя
        message = input('>> ')
        if message.lower() == 'quit': # Выход из цикла
            sock.close()
            break
        send_message(sock, message)

def main():
    # Запрашиваем у пользователя порт, к которому нужно подключиться
    server_port = int(input('Enter server port: '))
    # Создаем сокет и подключаемся к серверу
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, server_port))

    print(f'Connected to {SERVER_HOST}:{server_port}')

    # Запускаем два потока - один для чтения ввода пользователя, другой для обработки сообщений от сервера
    server_thread = threading.Thread(target=handle_server_messages, args=(sock,))
    user_thread = threading.Thread(target=handle_user_input, args=(sock,))
    server_thread.start()
    user_thread.start()
    server_thread.join()
    user_thread.join()

if __name__ == '__main__':
    main()
 

input()