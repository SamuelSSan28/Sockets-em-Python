from datetime import datetime
from BD_2 import BancoDeDados


def diff_tempo(ultimo_registro):
    time_stamp = datetime.strptime(ultimo_registro, '%d/%m/%Y %H:%M:%S')
    data_e_hora_atuais = datetime.now()
    dif = (data_e_hora_atuais - time_stamp)
    return  dif.total_seconds()


def clima():
    import requests
    import json
    '''
    :Function: Faz um GET com a API pra receber as informações de uma cidade
    :return: Retorna uma lista cotendo o clima e a temperatura(°c)
    '''
    req = "https://api.weatherbit.io/v2.0/current?city=Teresina,BR&key=89ff6003e58e45e69116346b6df12f54"
    try:
        resp = requests.get(req)
        print(resp,end = '   ')
        r =  json.loads(resp.text)
        c = [r['data'][0]['temp'] ,r['data'][0]['rh'],r['data'][0]['app_temp'],r['data'][0]['ob_time']]

        return c
    except Exception as e:
        print("ERRO:", e)
        return None

def dataHora():
    '''
    :return: Retorna a data e a hora do PC no momento
    '''
    data_e_hora_atuais = datetime.now()
    #print(data_e_hora_atuais)
    return data_e_hora_atuais.strftime("%d/%m/%Y %H:%M:%S").split()

def insereTempAPI(data,horarioM,horarioR,temp,humi,sensTermic): # insere dados na tabela registros
    # Abrimos uma conexão com o banco de dados:
    bd = BancoDeDados()
    c = bd.conexaoBD()

    # Cria um cursor:
    cursor = c.cursor()

    # Executa o comando:
    sql  = "INSERT INTO registros_temp_cidade (temperatura,humidade,sensacao_termica,dia,horario_medicao,horario_registro) VALUES (%s,%s,%s,%s,%s,%s)"
    val = [temp,humi,sensTermic,data,horarioM,horarioR]
    cursor.execute(sql,val)


    # Efetua um commit no banco de dados.
    # Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar
    # suas alterações.
    c.commit()

    # fecha conexao
    c.close()


#-------------------------main---------------------------------
print("Servidor API On")
atual = dataHora()
while True:
    try:
        if diff_tempo(atual[0]+' '+atual[1]) >= 900 and clima():
            temp,humi,sensacao,horarioM = clima()
            atual = dataHora()
            print(atual)
            insereTempAPI(atual[0],horarioM,atual[1],temp,humi,sensacao)
    except Exception as err:
        print('Error:' ,err)
        d,h = dataHora()
        e = "Error: {0} no dia ".format(err) + d + " as " +h +"\n"
        arq = open('log_api.txt', 'a+')
        arq.write(e)
        arq.close()
        continue
