import mariadb
import sys
from Config import Config 

try:
    config = Config(True).vars
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
cursor.execute("SELECT hash_id, nome, sobrenome, email FROM mailing WHERE ativo = 1 ORDER BY nome ASC")

res = cursor.fetchall()

header = ["hash", "Nome", "Sobrenome", "Email"]

f = open("backup_mailing_jan_2023_2.csv", "w")
f.write(header[0]+";"+header[1]+";"+header[2]+";"+header[3]+";\n")

for row in res:
    strg = ""
    for data in row:
        strg += data+";"
    strg += "\n"
    f.write(strg)

f.close()


    