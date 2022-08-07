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

def save_register(line, salt):
    register = line.replace("\n", "").split(";")
    if register[2] == "Email":
        return False
    hashid = sha256((register[2]+salt).encode('utf-8')).hexdigest()
    try:
        cursor.execute(insert, (hashid, register[0], register[1], register[2]))
        return True
    except mariadb.Error as e:
        return False

inseridos = 0
repetidos = 0
file = open("backup_mailing.csv", "r")
while True:
    line = file.readline()
    if line == "": 
        break
    if not save_register(line, config['salt']):
        repetidos += 1
    else:
        inseridos += 1

print("Inseridos: "+str(inseridos))
print("Repetidos: "+str(repetidos))

conn.commit()
conn.close()