import socket
from BD_2 import BancoDeDados
from datetime import datetime


def dataHora():
    '''
    :return: Retorna  um vetor com a data na primeira posição e a hora na segunda. As duas então no formato convecional e são do tipo string.
    '''
    data_e_hora_atuais = datetime.now()  # recebe a data e hora atuais
    return data_e_hora_atuais.strftime("%d/%m/%Y %H:%M:%S").split()


def recebe_e_filtra_msg(con):
    '''
    :param con: conexao socket aberta no momento
    :return: mensagem recebida decodificada de binario para string
    '''
    m = ''
    msg = con.recv(1024)
    m = str(msg, 'cp437').split()
    while not (b'fim' in msg):
        msg = con.recv(1024)
        if not msg: return
        m = str(msg, 'cp437').split()  # decodificando a msg

    con.close()

    m.pop(-1)  # remove a ultima palavra da string que é uma msg de controle
    m.pop(0)  # remove a primeira palavra da string que é o tipo do sensor pq esse script é só pra sensores entao todos são 0
    data, horario = dataHora()  # data e horario que a msg foi recebida
    m.append(data)  # adiciona  o horario que a msg foi recebida
    m.append(horario)  # adiciona a data que a msg foi recebida
    return m


def envia_pro_BD(registros,id_node):
    '''
    :param registros: os dados que vão ser inseridos no BD
    :return:
    '''
    bd = BancoDeDados()
    soma_temp = 0
    soma_umi = 0
    soma_corrente = 0

    for msg in registros[id_node]:
        if not (msg[1] or msg[2] or msg[3]):
        	break
        soma_temp += float(msg[1])
        soma_umi += float(msg[3])
        soma_corrente += float(msg[2])

    msg = registros[id_node][-1]  # ultima mensagem adicioanda a lista
    med_temp = round(soma_temp / len(registros[id_node]), 3)
    med_umi = round(soma_umi / len(registros[id_node]), 3)
    sum_corrente = round(soma_corrente, 3)

    if bd.buscaNo(msg[0]):
        bd.insereDados_Sensores(msg[0], msg[4], msg[5], str(med_temp), str(sum_corrente), str(med_umi)) #armazena dados no BD
    else:
        bd.insereNodes(msg[0], 0)  #armazena novo nó no BD
        bd.insereDados_Sensores(msg[0], msg[4], msg[5], str(med_temp), str(sum_corrente), str(med_umi)) #armazena dados no BD

    registros[id_node] = []


def main():
    '''
        responsavel por gerenciar os processos de receber,filtrar e armazenar os registros dos sensores de temperatura  e corrente
    '''

    HOST = '10.94.15.69'  # Endereco IP do Servidor
    PORT = 9999  # Porta que o Servidor está

    sensores = {}  # dicionario com a lista de sensores e seus registros
    controle = ''

    tempo_controle = dataHora()  # pegando data e hora atual

    # comentar
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind((HOST, PORT))
    tcp.listen(7)

    print("Servidor On")
    print(dataHora())

    while True:
        try:
            try:
                con, cliente = tcp.accept()  # aceita uma conexão com um cliente
                msg = recebe_e_filtra_msg(con)  # recebe a msg eviada pelo cliente
            except Exception as err:
                try:
                    con.close()  # tenta fechar a conexexão caso tenha acontecido algum erro
                except Exception as err:
                    print("Não conseguiu fechar a conexao")

                d, h = dataHora()
                e = "  Error: {0} no dia".format(err) + d + " as " + h + '\n'
                arq = open('log.txt', 'a+')
                arq.write(e)
                arq.close()
                print(e)
                continue

            if not msg: continue

            if msg[0] in sensores:  # se id já é conhecido
                #print(msg[0],msg)
                sensores[msg[0]].append(msg)  # adiciona a mensagem na id
                if len(sensores[msg[0]]) == 6 and msg[0] != '4':  # se já tem 6 registros (1 minuto)
                    envia_pro_BD(sensores,msg[0])  # armazena os dados
                elif len(sensores[msg[0]]) == 12 and msg[0] == '4':# se já tem 12 registros de 5 SEGUNDOS (1 minuto)
                	envia_pro_BD(sensores,msg[0])  # armazena os dados
            else:
                sensores.update({msg[0]: []})
                sensores[msg[0]].append(msg)


        except Exception as err:
            d, h = dataHora()
            e = "  Error: {0} no dia ".format(err) + d + " as " + h + "\n"
            arq = open('log.txt', 'a+')
            arq.write(e)
            arq.close()
            print(e)
            continue


main()