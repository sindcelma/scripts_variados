import mariadb
import sys
from Config import Config 
from hashlib import sha256

emails = [
    {
        "nome":"Luis",
        "sobrenome":"Reis",
        "email":"luisreis@suzano.com.br"
    },
    {
        "nome":"Andre",
        "sobrenome":"Fernandes da Silva",
        "email":"fernandesdasilvaandre78@gmail.com"
    }
]

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


for reg in emails:
    save_register(reg['nome'], reg['sobrenome'], reg['email'])

conn.commit()
conn.close()