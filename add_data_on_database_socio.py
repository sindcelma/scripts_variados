import mariadb
import sys
from Config import Config 

try:
    config = Config().vars
    conn = mariadb.connect(
        user=config['user'],
        password=config['password'],
        host=config['host'],
        port=config['port'],
        database=config['database']
    )
except mariadb.Error as e:
    print(f"Error to connect {e}")
    sys.exit(1)

cursorSel = conn.cursor()

sociosSelect = cursorSel.execute("SELECT id FROM socios")
socios = cursorSel.fetchall()

insertPessoaisStr = "INSERT INTO socios_dados_pessoais (socio_id) VALUES "
insertProfissStr  = "INSERT INTO socios_dados_profissionais (empresa_id, socio_id) VALUES "

for socio in socios:
    insertPessoaisStr += "("+str(socio[0])+"),"
    insertProfissStr  += "(1, "+str(socio[0])+"),"

insertPessoaisStr = insertPessoaisStr[:len(insertPessoaisStr)-1]
insertProfissStr  =  insertProfissStr[:len(insertProfissStr)-1]

cursorInsertPessoais = conn.cursor()
cursorInsertProfiss  = conn.cursor()

cursorInsertPessoais.execute(insertPessoaisStr)
cursorInsertProfiss.execute(insertProfissStr)


conn.commit()
conn.close()