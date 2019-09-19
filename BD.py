# Importamos a biblioteca:
import pymysql

class BancoDeDados:

    def dadosServ(self):
        arquivo = open('data.txt', 'r')
        dados = ''
        for i in arquivo:
            dados = i

        return dados.split()


    def conexaoBD(self): #retorna uma conexao com o BD
        dados = self.dadosServ()
        return pymysql.connect(db=dados[0], user=dados[1], passwd=dados[2])


    def buscaNo(self,ip):
        # Abrimos uma conexão com o banco de dados:
        c = self.conexaoBD()
        # Cria um cursor:
        cursor = c.cursor()

        # Executa o comando:
        cmd = "SELECT ip,mac,tipo FROM nodes WHERE ip = '"+ip+"'"
        cursor.execute(cmd)

        # Recupera o resultado:
        resultado = cursor.fetchall()

        # Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar suas alterações.
        c.commit()

        #fecha conexao
        c.close()

        return  not (resultado == ())

    def buscaSensor(self,ip):
        # Abrimos uma conexão com o banco de dados:
        c = self.conexaoBD()
        # Cria um cursor:
        cursor = c.cursor()

        # Executa o comando:
        cmd = "SELECT temperatura_sala,umidade FROM registros_sensores WHERE ip_node = '"+ip+"'"
        cursor.execute(cmd)

        # Recupera o resultado:
        resultado = cursor.fetchall()

        # Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar suas alterações.
        c.commit()

        #fecha conexao
        c.close()

        return  (resultado)


    def insereDados_Sensores(self,ip,data,horario,temp,corrente,umidade): # insere dados na tabela registros
        # Abrimos uma conexão com o banco de dados:
        c = self.conexaoBD()

        # Cria um cursor:
        cursor = c.cursor()

        # Executa o comando:
        cmd = "INSERT INTO registros_sensores (ip_Node,dia,horario,temperatura_sala,corrente,umidade) VALUES ('"+ip+"','"+data+"','"+horario+"','"+temp+"','"+corrente+"','"+umidade+"')"
        cursor.execute(cmd)

        # Efetua um commit no banco de dados.
        # Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar
        # suas alterações.
        c.commit()

        # fecha conexao
        c.close()



    def insereDados_Controle(self,ip,data,horario,temp,estado): # insere dados na tabela registros
        # Abrimos uma conexão com o banco de dados:
        #print(ip, data, horario, temp, estado)
        c = self.conexaoBD()

        # Cria um cursor:
        cursor = c.cursor()

        # Executa o comando:
        #import pdb; pdb.set_trace()

        cmd = "INSERT INTO registros_controle (ip_Node,dia,horario,temperatura,estado) VALUES ('"+ip+"','"+data+"','"+horario+"','"+temp+"','"+estado+"')"
        cursor.execute(cmd)

        # Efetua um commit no banco de dados.
        # Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar
        # suas alterações.
        c.commit()

        # fecha conexao
        c.close()

    def alteraDados_Controle(self,ip,data,horario,horario2,temp): # insere dados na tabela registros
        # Abrimos uma conexão com o banco de dados:
        c = self.conexaoBD()

        # Cria um cursor:
        cursor = c.cursor()

        # Executa o comando:
        #import pdb; pdb.set_trace()
        sql = "UPDATE registros_controle SET horario =%s,temperatura=%s  WHERE ip_Node = %s AND dia = %s AND horario =%s"
        val = [horario2,temp,ip,data,horario]

        #cmd = "UPDATE registros_sensores SET ip_Node = '"+ip+"',dia ='" + ""+"',horario ='" + "'"

        cursor.execute(sql,val)

        # Efetua um commit no banco de dados.
        # Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar
        # suas alterações.
        c.commit()

        # fecha conexao
        c.close()


    def insereNodes(self,ip,mac,tipo):
        # Abrimos uma conexão com o banco de dados:
        c = self.conexaoBD()

        # Cria um cursor:
        cursor = c.cursor()

        # Executa o comando:
        cmd = "INSERT INTO nodes (ip,mac,tipo) VALUES ('" + ip + "','" + mac +"','"+ str(tipo) +"')"
        cursor.execute(cmd)

        # Efetua um commit no banco de dados.
        # Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar
        # suas alterações.
        c.commit()

        # fecha conexao
        c.close()


    def clear_All(self):
        # Abrimos uma conexão com o banco de dados:
        c = self.conexaoBD()

        # Cria um cursor:
        cursor = c.cursor()

        # Executa o comando:
        cmd = "DElETE  FROM nodes "
        cursor.execute(cmd)

        cmd = "DElETE  FROM registros_sensores "
        cursor.execute(cmd)

        cmd = "DElETE  FROM registros_controle "
        cursor.execute(cmd)

        # Efetua um commit no banco de dados.
        # Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar
        # suas alterações.
        c.commit()

        # fecha conexao
        c.close()

#a = BancoDeDados()
#a.clear_All()

