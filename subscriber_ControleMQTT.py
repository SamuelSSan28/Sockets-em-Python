from datetime import datetime
import sys
import paho.mqtt.client as mqtt
import sqlite3
from BD_2 import BancoDeDados

broker = "10.94.15.69"
port = 1883
keppAlive = 60
topic = 'controleAc/Disnel/temp_est_bd'

# funcao responsavel por cadastrar no banco de dados a temperatura do sensor
def insertTemperature(temp,estado):
    bd = BancoDeDados()
    dh = dataHora()
    bd.insereDados_Controle(str(4),dh[0],dh[1],temp,estado)

def on_connect(client, userdata, flags, rc):
    client.subscribe(topic)


def dataHora():
    '''
    :return: Retorna a data e a hora do PC no momento
    '''
    data_e_hora_atuais = datetime.now()
    print(data_e_hora_atuais)
    return data_e_hora_atuais.strftime("%d/%m/%Y %H:%M:%S").split()


def on_message(client, userdata, msg):
    message = str(msg.payload) # converte a mensagem recebida
    try :
        param = message[2:6].split(" ")
        insertTemperature(param[0],param[1])# invoca o metodo de cadastro passando por parametro a temperatura recebida
    except Exception as e:
        print(message[2:6].split(" "),e)
        exit(0)

try:
    print("Controle MQTT...")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # client.connect(broker, port, keppAlive)
    client.connect(broker)
    client.username_pw_set("mqtt_user", "mqtt_ufpi")
    client.loop_forever()

except KeyboardInterrupt:
    print ("\nScript finalizado.")
    sys.exit(0)
