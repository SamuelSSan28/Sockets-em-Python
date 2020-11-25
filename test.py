import socket, threading

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print("New connection added: ", clientAddress)

    def run(self):
        print("Connection from : ", clientAddress)
        # self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        msg = ''
        while True:
            data = self.csocket.recv(1024)
            msg = data.decode()
            if msg == ' ':
                continue
            print("--",msg)
            self.csocket.send(bytes(msg, 'UTF-8'))
        print("Client at ", clientAddress, " disconnected...")


LOCALHOST = "10.94.15.69"
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")

while True:
    server.listen(5)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
