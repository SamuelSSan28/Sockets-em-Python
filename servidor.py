import socket
from BD import BancoDeDados
from datetime import datetime
from datetime import timedelta

def dataHora():
    '''
    :return: Retorna a data e a hora do PC noomrnto
    '''
    data_e_hora_atuais = datetime.now()
    return data_e_hora_atuais.strftime("%d/%m/%Y %H:%M:%S").split()

def hora():
    '''
    :return: Retorna a hora do PC noomrnto
    '''
    data_e_hora_atuais = datetime.now()
    return data_e_hora_atuais.strftime("%H:%M:%S")


def dadosServ():
    '''
    :return: Leitura dos dados fo servidor
    '''
    arquivo = open('data.txt', 'r')
    dados = ''
    for i in arquivo:
        dados = i

    return dados.split()


def recebe_msg(con):
    m = ''
    msg = con.recv(1024)
    m = str(msg, 'cp437').split()
    if len(m) > 0:
        if m[0] == '2':
            return m
    while not (b'fim' in msg):
        msg = con.recv(1024)
        if not msg: return
        m = str(msg, 'cp437').split()


    con.close()

    return m


def envia_pro_BD(tipo,registros):
    bd = BancoDeDados()

    if(tipo):
        aux = registros[6]
        ultimo = aux[1].split(':')
        #import pdb; pdb.set_trace()
        ultimo = timedelta(days = 0, hours = int(ultimo[0]), minutes = int(ultimo[1]),seconds=int(ultimo[2]))
        novo = registros[5].split(':')
        novo = timedelta(days = 0, hours = int(novo[0]), minutes = int(novo[1]),seconds=int(novo[2]))
        result = novo - ultimo

        if result.total_seconds() < 20: #ajustar
            bd.alteraDados_Controle(registros[3], aux[0], aux[1], registros[5], registros[1])
        else:
            bd.insereDados_Controle(registros[3],registros[4],registros[5],registros[1],registros[2])



    else:
        reg = []
        for i in registros:
            if len(registros[i]) == 6: #condicao para mandar pro servidor
                med_temp = 0
                med_umi = 0
                for j in registros[i]:
                    med_temp += float(j[1])
                    med_umi += float(j[3])

                med_temp = med_temp /6
                med_umi = med_umi /6

                if bd.buscaNo(j[4]):
                    bd.insereDados_Sensores(j[4], j[5], j[6], str(med_temp), j[2], str(med_umi))
                else:
                    bd.insereNodes(j[4], 'teste', tipo)
                    bd.insereDados_Sensores(j[4], j[5], j[6], j[1], j[2], j[3])


                registros[i] = []



def controlador(con,ip,msg):
    """
        Vai ser responsavel por filtrar as mensagens que chegam
    """

    msg.pop(-1)  # remove a ultima palavra da string que é uma msg de controle
    t = msg.pop(0)  # remove a primeira palavra da string que é o codigo do tipo de msg

    if t == '0': #Nós que estão coletando temperatura/corrente
        data, horario = dataHora()  # horario
        msg.append(ip)
        msg.append(data)
        msg.append(horario)
        #print(msg)

    elif t == '1':#Nó controle do Ar
        data, horario = dataHora()  # horario
        msg.append(ip)
        msg.append(data)
        msg.append(horario)

    return int(t),msg




#-------------main-----------------
dados = dadosServ()
conectados = [] # lista de nodes que estão conectados

HOST = dados[3]  # Endereco IP do Servidor
PORT = int(dados[4] ) # Porta que o Servidor está

sensores = {}
controle = ''
tempo_controle = dataHora()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(10)

print("Servidor ON")


while True:
    con, cliente = tcp.accept()
    tcp.sendto(b'1', cliente)
    a = recebe_msg(con)
    if not a: continue

    t,msg = controlador(con,cliente[0],a) #   t: tipo de msg       msg: a mensagem


    if t == 1 :
        msg.append(tempo_controle)
        controle = cliente
        envia_pro_BD(t, msg)
        print("Controle ->",msg)
        tempo_controle = (msg[4] + " " + msg[5]).split()

    if cliente[0] in sensores and t == 0: #se ip já é conhecido
            sensores[cliente[0]].append(msg)
            if len(sensores[cliente[0]]) == 6:
                print("Media ->",msg)
            envia_pro_BD(t, sensores)
    elif t == 0:
            sensores.update({cliente[0]: []})
            sensores[cliente[0]].append(msg)
            envia_pro_BD(t, sensores)

    elif t == 2:
        if(controle != ''):
            print(controle)
            tcp.sendto(b'1',controle)



