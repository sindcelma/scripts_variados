import mariadb
import sys
from Config import Config 
from datetime import datetime

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

cursor = conn.cursor()
cursor.execute("SELECT nome, sobrenome, email, ativo FROM mailing WHERE ativo = 1")

res = cursor.fetchall()

header = ["Nome", "Sobrenome", "Email", "status"]
status = ["descadastrado", "ativo", "desativado"]

data_e_hora_atuais = datetime.now()
data_e_hora_em_texto = data_e_hora_atuais.strftime('%d_%m_%Y___%H_%M')
f = open("backup_mailing_ativos_"+data_e_hora_em_texto+".csv", "w")
f.write(header[0]+";"+header[1]+";"+header[2]+";"+header[3]+";\n")

for row in res:
    st = status[row[3]]
    f.write(row[0]+";"+row[1]+";"+row[2]+";"+st+";\n")

f.close()


    