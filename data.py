# Importamos a biblioteca:
import pymysql
import matplotlib.pyplot as plt



def conexaoBD():  # retorna uma conexao com o BD
    # sensores temperatura DisnelLab2019
    return pymysql.connect(db='sensores_2', user='temperatura', passwd='DisnelLab2019')

def busca_Dados_CORRENTE(dia_i,horario_i,horario_f):
        # Abrimos uma conexão com o banco de dados:
        c = conexaoBD()
        # Cria um cursor:
        cursor = c.cursor()

        # Executa o comando:
        cmd = "SELECT round(sum(corrente)) FROM registros_sensores WHERE dia = %s and horario >= %s  and horario <= %s ;"
        val = [dia_i, horario_i,horario_f]

        cursor.execute(cmd, val)

        # Recupera o resultado:
        resultado = cursor.fetchall()

        # Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar suas alterações.
        c.commit()

        #fecha conexao
        c.close()

        return  resultado


def busca_Dados_TEMPERATURA_e_UMIDADE(dia_i, horario_i, horario_f):
    # Abrimos uma conexão com o banco de dados:
    c = conexaoBD()
    # Cria um cursor:
    cursor = c.cursor()

    # Executa o comando:
    cmd = "SELECT ROUND(avg(temperatura)),ROUND(avg(umidade)) FROM sensores_2.registros_sensores WHERE dia = %s and horario >= %s  and horario <= %s ;"
    val = [dia_i, horario_i, horario_f]

    cursor.execute(cmd, val)

    # Recupera o resultado:
    resultado = cursor.fetchall()

    # Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar suas alterações.
    c.commit()

    # fecha conexao
    c.close()

    return resultado


corrente_acumulada_pHora = []
temperatura_media_pHora = []
umidade_media_pHora = []
horas = []
h1 = ["00:00:00","01:00:00","02:00:00","03:00:00","04:00:00","05:00:00","06:00:00","07:00:00","08:00:00","09:00:00","10:00:00","11:00:00","12:00:00","13:00:00","14:00:00","15:00:00","16:00:00","17:00:00","18:00:00","19:00:00","20:00:00","21:00:00","22:00:00","23:00:00"]
h2 = ["00:59:59","01:59:59","02:59:59","03:59:59","04:59:59","05:59:59","06:59:59","07:59:59","08:59:59","09:59:59","10:59:59","11:59:59","12:59:59","13:59:59","14:59:59","15:59:59","16:59:59","17:59:59","18:59:59","19:59:59","20:59:59","21:59:59","22:59:59","23:59:59"]
for i in range(24):
        #print(h1[i],h2[i],"--",end = '')
        a = busca_Dados_CORRENTE("10/10/2019",h1[i],h2[i])
        b = busca_Dados_TEMPERATURA_e_UMIDADE("10/10/2019",h1[i],h2[i])
        #print(a)
        #print(b)
        if type(a[0][0]) == float:
            corrente_acumulada_pHora.append(int(a[0][0]))
            temperatura_media_pHora.append(b[0][0])
            umidade_media_pHora.append(int(b[0][1]))
            h = h1[i][0:2]
            horas.append(h)


plt.bar(horas, corrente_acumulada_pHora)
plt.ylabel("Corrente")
plt.xlabel("Horas")
plt.show()

plt.bar(horas, umidade_media_pHora,color='blue')
plt.ylabel("Humidade")
plt.xlabel("Horas")
plt.show()

plt.bar(horas, temperatura_media_pHora,color='red' )
plt.ylabel("Temperatura")
plt.xlabel("Horas")
plt.show()