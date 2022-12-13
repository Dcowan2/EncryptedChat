import socket
import threading
from cryptography.fernet import Fernet

key = Fernet.generate_key()


class Client:

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while 1:
            try:
                host = input('Enter host name --> ')
                port = int(input('Enter port --> '))
                self.s.connect((host, port))

                break
            except:
                print("Couldn't connect to server")

        self.username = input('Enter username --> ')
        self.s.send(self.username.encode())

        self.s.send(key)

        message_handler = threading.Thread(target=self.handle_messages, args=())
        message_handler.start()

        input_handler = threading.Thread(target=self.input_handler, args=())
        input_handler.start()

    def handle_messages(self):
        while 1:
            f = Fernet(key)
            print(f.decrypt(self.s.recv(1204)))

    def input_handler(self):
        while 1:
            msg = input().encode()
            f = Fernet(key)
            msg = f.encrypt(msg)
            self.s.send(msg)


client = Client()
