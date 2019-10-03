import datetime
import socket




HOST = '10.94.15.69'  # Endereco IP do Servidor
PORT = 9999 # Porta que o Servidor está

sensores = {}
controle = ''


tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(10)

print("Servidor ON")

while True:
    con, cliente = tcp.accept()
    msg = con.recv(1024)
    m = str(msg, 'cp437').split()

    while not (b'fim' in msg):
        msg = con.recv(1024)
        if not msg: continue
        m = str(msg, 'cp437').split()

    print(m)
    con.close()



