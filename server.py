import socket
import select

header_lenght = 10
IP = '127.0.0.1'
PORT = 5051

import socket
import select

HEADER_LENGTH = 100

IP = "127.0.0.1"
PORT = 1234

# Создаем сокет
# socket.AF_INET - адрес IPv4
# socket.SOCK_STREAM - TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Настройка сокета
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# задаем серверу ip и порт
server_socket.bind((IP, PORT))

# Можно обслуживать новые подключения
server_socket.listen()

# Список всех сокетов
sockets_list = [server_socket]

# Словарь пользователей, где ключ - сокет, а вот "user header" и имя - данные
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')

# Получаем сообщения
def receive_message(client_socket):

    try:

        # Отправляем "header"
        message_header = client_socket.recv(HEADER_LENGTH)

        # Если нет данных - клиент закрывается
        if not len(message_header):
            return False

        # Конвертируем "header" в int
        message_length = int(message_header.decode('utf-8').strip())

        
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:

        # Потеря соединения
        return False

while True:

    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)


    for notified_socket in read_sockets:

        # Новый сокет
        if notified_socket == server_socket:

            client_socket, client_address = server_socket.accept()

            # Клиент отправляет свой ник
            user = receive_message(client_socket)

            # В ином случае - дисконект
            if user is False:
                continue

            # Исключение
            sockets_list.append(client_socket)

            # Сохраняем ник
            clients[client_socket] = user

            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

        # Отправка сообщений
        else:

            message = receive_message(notified_socket)

            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                sockets_list.remove(notified_socket)

                del clients[notified_socket]

                continue

            user = clients[notified_socket]

            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            for client_socket in clients:

                if client_socket != notified_socket:

                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:

        sockets_list.remove(notified_socket)

        del clients[notified_socket]
