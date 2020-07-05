import socket
import threading

# Предлагаем ввести свой никнейм
while True:
	nickname = input("Choose your nickname: ").strip()
	if bool(nickname) is False:
		print("Your input must have at least 1 character.")
		continue
	else:
		break


# Подключаемся к серверу
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 16180))

# Получаем сообщения от сервера и отправляем свой ник
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'CHECK@NICKNAME':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            # Закрывает соединение при возникновении какой-либо ошибки
            print("Error!")
            client.close()
            break

# Отправка сообщений серверу
def sending():
	while True:
		message = '{}: {}'.format(nickname, input(''))
		client.send(message.encode('utf-8'))

# Создаем многопоточность функций recieve() и sending()
receive_thread = threading.Thread(target=receive)
receive_thread.start()

sending_thread = threading.Thread(target=sending)
sending_thread.start()
