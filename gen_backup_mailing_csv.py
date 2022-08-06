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

cursor = conn.cursor()
cursor.execute("SELECT nome, sobrenome, email FROM mailing WHERE ativo = 1")

res = cursor.fetchall()

header = ["Nome", "Sobrenome", "Email"]

f = open("backup_mailing.csv", "w")
f.write(header[0]+";"+header[1]+";"+header[2]+";\n")

for row in res:
    strg = ""
    for data in row:
        strg += data+";"
    strg += "\n"
    f.write(strg)

f.close()


    