import socket
import threading  # выполнение различных задач одновременно !!!

# Данные для соединения
host = '127.0.0.1'  # IP адресс для хоста
port = 16180  # Порт хоста

# Запускаем сервер
'''
- Определяем тип сокета

	Параметры:

	1. socket.AF_INET - указывает на то, что мы используем интернет сокет (то есть сокет IP), а не UNIX сокет
		"Сокет UNIX - представляет собой механизм межпроцессного взаимодействия , который позволяет осуществлять обмен данными между двунаправленных процессов , работающих на одной и той же машине."

	2. socket.SOCK_STREAM - указывает на протокол TCP, который мы будем использовать (а не UDP)

- Привязываем сокет к хосту и порту (IP, PORT), передавая значения в типе данных tuple

- Переводим сервер в режим listening - он будет ожидать подключения клиентов
'''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen()

# Создаем пустые списки клиентов, никнеймов, буфферный список клиентов
clients = []
nicknames = []


# Функция, которая просто отправляет сообщения каждому пользователю в списке пользователей
def broadcast(message):
	for client in clients:
		client.send(message)



# Обработка сообщений пользователей. Обнаружение отсоединения пользователя от сервера.
def handle(client):
    while True:
        try:
            # Получем сообщение от пользователя и отправляем его остальным
            message = client.recv(1024)
            broadcast(message)
        except:
            # Если по какой-то причине возникает ошибка подключения к
            # пользователю - мы удаляем его из списка клиентов и никнеймов,
            # выводим сообщение "{его ник} left!", завершаем цикл.
            index = clients.index(client)
            clients.remove(client)
            client.close()  # закрываем сокет
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break


# Основная функция, в которой задействуется бесконечный цикл. recieve()
# вызывается при запуске сервера, в ней же вызываются все, созданные выше,
# функции.
def receive():
    while True:
        '''
        Соединяем клиента (при таковом подключении)
        "Accept a connection. The socket must be bound to an address and listening for connections. The return value is a pair (conn, address) where conn is a new socket object usable to send and receive data on the connection, and address is the address bound to the socket on the other end of the connection." (С) Из документации к модулю socket.
        '''
        client, address = server.accept()
        # Сообщение выводится, соответсвенно, только на сервере
        print("Connected with {}".format(str(address)))

        # Запрос на создание никнейма и запись его в список (а также запись
        # сокет обьекта "клиент" в список клиентов)
        client.send('CHECK@NICKNAME'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # Представляем нашего пользователся участникам чата.
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('utf-8'))

        # Многопоточность выполнения функции handle(client)
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
