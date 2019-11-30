import time

from BD_2 import BancoDeDados
from datetime import datetime
import paho.mqtt.client as paho
# import pdb; pdb.set_trace() #classe de teste
class Controle:
    def __init__(self):
        self.bd = BancoDeDados()

    def dataHora(self):
        '''
        :return: Retorna a data e a hora do PC no momento
        '''
        data_e_hora_atuais = datetime.now()
        return data_e_hora_atuais.strftime("%d/%m/%Y %H:%M:%S").split()

    def publish(self,topic,msg):
        broker_address = "10.94.15.69"
        port = 1883
        client = paho.Client("ControlDeDanos")  # create new instance

        client.on_connect = self.on_connect  # attach function to callback
        client.connect(broker_address, port=port)
        client.loop_start()

        client.publish(topic, msg)

        client.disconnect()
        client.loop_stop()

    def on_connect(client, userdata, flags, rc):

        if rc == 0:

            print("Connected to broker")

            global Connected  # Use global variable
            Connected = True  # Signal connection

        else:

            print("Connection failed")

    def consultaSensores(self):
        # abre conexao
        con = self.bd.conexaoBD()

        # Cria um cursor:
        cursor = con.cursor()

        # Executa o comando
        cmd = "select * from registros_sensores ORDER BY id_registro_sensor DESC limit 1"
        cursor.execute(cmd)

        # Recupera o resultado:
        resultado = cursor.fetchall()

        # Efetua um commit no banco de dados.
        # Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar suas alterações.
        con.commit()

        # fecha conexao
        con.close()
        return resultado

    def consultaNodes(self):
        # abre conexao
        con = self.bd.conexaoBD()

        # Cria um cursor:
        cursor = con.cursor()

        # Executa o comando
        cmd = "select * from nodes"
        cursor.execute(cmd)

        # Recupera o resultado:
        resultado = cursor.fetchall()


        # Efetua um commit no banco de dados.
        # Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar suas alterações.
        con.commit()

        # fecha conexao
        con.close()
        return resultado

    def consultaControle(self):
        # abre conexao
        con = self.bd.conexaoBD()

        # Cria um cursor:
        cursor = con.cursor()

        # Executa o comando
        cmd = "select * from registros_controle ORDER BY id_registro_controle DESC limit 1"
        cursor.execute(cmd)

        # Recupera o resultado:
        resultadoC = cursor.fetchall()

        # Executa o comando
        cmd = "select * from registros_sensores ORDER BY id_registro_sensor DESC limit 1"
        cursor.execute(cmd)

        # Recupera o resultado:
        resultadoS = cursor.fetchall()


        # Efetua um commit no banco de dados.
        # Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar suas alterações.
        con.commit()

        # fecha conexao
        con.close()
        return resultadoS,resultadoC

    def verificaQuedas(self,antigo):
        dados = self.consultaSensores()
        d, h = self.dataHora()
        e =''
        ultimo_registro = dados[0][3]+ " "+ dados[0][4]
        time_stamp  = datetime.strptime(ultimo_registro, '%d/%m/%Y %H:%M:%S')
        data_e_hora_atuais = datetime.now()
        dif = (data_e_hora_atuais-time_stamp)
        dif = dif.total_seconds()

        if dif > 70 and e != antigo:
            e = "Error: Servidor caiu"
            self.publish("servidor/logQuedas", e+" no dia " + d + " as " + h + "\n")
            arq = open('logControle.txt', 'a+')
            arq.write(e)
            arq.close()

        elif antigo != "Servidor On":
            e = "Servidor On"
            self.publish("servidor/logQuedas",e)
        else:
            return antigo
        return e

    def verificaSensorInativo(self,antigo):
        nodes = self.consultaNodes()
        registros = self.consultaSensores()
        lista_nodes =[]
        for i in nodes:
            if i[0] != 5:
                lista_nodes.append(i[0])

        lista_ativos = []
        for i in registros[len(registros)-4:]:
            lista_ativos.append(i[6])

        msg = ''
        for i in lista_nodes:
            if i in lista_ativos:
                msg += str(i)+":On "
            else:
                msg += str(i) + ":Off "


        if (antigo != msg):
            self.publish("servidor/Nodes",msg)
            d, h = self.dataHora()
            arq = open('logControle.txt', 'a+')
            arq.write(msg+ d + " as " + h + "\n")
            arq.close()
        else:
            return antigo

        return msg

    def verificaControle_ligar_desligar(self,antigo):
        corrente,controle = self.consultaControle()
        msg = ''
        if controle[0][2] == 1 and corrente[0][5] < 0.5 and antigo != "Esta ligado mas a corrente esta baixa":
            msg = "Esta ligado mas a corrente esta baixa"
            self.publish("servidor/controleEcorrente",msg)
            arq = open('logControle.txt', 'a+')
            arq.write("Esta ligado mas a corrente esta baixa\n")
            arq.close()

        elif controle[0][2] == 0 and corrente[0][5] > 0.5 and antigo != "Esta desligado mas a corrente esta alta":
            msg ="Esta desligado mas a corrente esta alta"
            self.publish("servidor/controleEcorrente",msg)
            arq = open('logControle.txt', 'a+')
            arq.write("Erro: Esta desligado mas a corrente esta alta\n")
            arq.close()

        elif antigo != "ok":
            msg = "ok"
            self.publish("servidor/controleEcorrente",msg)
        else:
            return antigo

        return  msg


a = Controle()
vsi = ""
vq = ""
vcld = ""

print("Controle de Danos ON")
while(True):
    vsi = a.verificaSensorInativo(vsi)
    vq = a.verificaQuedas(vq)
    vcld = a.verificaControle_ligar_desligar(vcld)
    time.sleep(30)