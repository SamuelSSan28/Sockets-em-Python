# Importamos a biblioteca:
import pymysql

class BancoDeDados:

    def dadosServ(self):
        arquivo = open('data.txt', 'r')
        dados = []
        for i in arquivo:
            dados.append(i)

        return dados

    def conexaoBD(self): #retorna uma conexao com o BD
        dados = self.dadosServ()
        return pymysql.connect(db=dados[0], user=dados[1], passwd=dados[2])

    def buscaNo(self,ip):
        # Abrimos uma conexão com o banco de dados:
        c = self.conexaoBD()
        # Cria um cursor:
        cursor = c.cursor()

        # Executa o comando:
        cmd = "SELECT ip,id,localizacao FROM nodes WHERE ip = '"+ip+"'"
        cursor.execute(cmd)

        # Recupera o resultado:
        resultado = cursor.fetchall()

        # Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar suas alterações.
        c.commit()

        #fecha conexao
        c.close()

        return  not (resultado == ())


    def insereDados(self,ip,data,horario,temp,corrente,umidade): # insere dados na tabela registros
        # Abrimos uma conexão com o banco de dados:
        c = self.conexaoBD()

        # Cria um cursor:
        cursor = c.cursor()

        # Executa o comando:
        cmd = "INSERT INTO registros (idNode,dia,horario,temperatura_sala,corrente,umidade) VALUES ('"+ip+"','"+data+"','"+horario+"','"+temp+"','"+corrente+"','"+umidade+"')"
        cursor.execute(cmd)

        # Efetua um commit no banco de dados.
        # Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar
        # suas alterações.
        c.commit()

        # fecha conexao
        c.close()


    def insereNodes(self,ip,local):
        # Abrimos uma conexão com o banco de dados:
        c = self.conexaoBD()

        # Cria um cursor:
        cursor = c.cursor()

        # Executa o comando:
        cmd = "INSERT INTO nodes (ip,localizacao) VALUES ('"+ip+"','"+local+"')"
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

        cmd = "DElETE  FROM registros "
        cursor.execute(cmd)

        # Efetua um commit no banco de dados.
        # Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar
        # suas alterações.
        c.commit()

        # fecha conexao
        c.close()



bd = BancoDeDados()

bd.conexaoBD()



