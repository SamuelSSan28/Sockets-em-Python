import socket
from BD import BancoDeDados
from datetime import datetime

class Dados:
    def __init__(self):
        self.IP  = ''
        self.local = ''
        self.temperatura = 0.0
        self.corrente = 1
        self.umidade = 0.0
        self.data = ''
        self.horario = ''

def sgbd(d = Dados()):
    bd = BancoDeDados()
    if bd.buscaNo(d.IP):
        bd.insereDados(d.IP,d.data,d.horario,d.temperatura,d.corrente,d.umidade)
    else:
        bd.insereNodes(d.IP,d.local)
        bd.insereDados(d.IP,d.data,d.horario,d.temperatura,d.corrente,d.umidade)

def dataHora():
    data_e_hora_atuais = datetime.now()
    return data_e_hora_atuais.strftime("%d/%m/%Y %H:%M").split()


def conectado(con, cliente):
    d = Dados()
    d.IP = cliente[0]

    msg = con.recv(1024)
    while not(b'fim' in msg):
        msg = con.recv(1024)
        m = str(msg,'cp437').split()

        '''--------------Coletando Dados------------'''
        d.local = m[0] #local
        d.temperatura = m[1]#temperatura
        d.corrente = m[2] #corrente
        d.umidade = m[3] #umidade
        d.data,d.horario = dataHora() #horario
        '''-----------------------------------------'''
        print(cliente[0],"enviou",m)

    con.close()
    return d




#-------------main-----------------
HOST = '10.94.15.69'   # Endereco IP do Servidor
PORT = 9999            # Porta que o Servidor esta

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(10)

print("Servidor ON")
while True:
    con, cliente = tcp.accept()
    d = conectado(con, cliente)
    sgbd(d)

tcp.close()
