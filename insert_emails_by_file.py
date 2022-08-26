from posixpath import split
import mariadb
import sys
from Config import Config 
from hashlib import sha256


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


insert = "INSERT INTO mailing (hash_id, nome, sobrenome, email) VALUES (?,?,?,?) "
cursor = conn.cursor()


def save_register(nome, sobrenome, email):
    hashid = sha256((email+config['salt']).encode('utf-8')).hexdigest()
    try:
        cursor.execute(insert, (hashid, nome, sobrenome, email))
        return True
    except mariadb.Error as e:
        return False


file    = open("backup_mailing_novos.csv", "r")
content = file.read()


for line in content.split("\n"):
    cline = line.split(";")
    if len(cline) > 1:
        nomefull = cline[1].split(" ", 1)
        sobrenome = nomefull[1] if len(nomefull) > 1 else ""
        nome = nomefull[0]
        email = cline[2]
        save_register(nome, sobrenome, email)


conn.commit()
conn.close()

