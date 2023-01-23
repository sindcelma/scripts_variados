import mariadb
import sys
import re 
from Config import Config 
import hashlib
import time
import random

def generateSlugAndSalt(salt=""):
    slug = hashlib.sha256((salt+str(round(time.time() * 1000))+str(random.random())).encode('utf-8')).hexdigest()
    salt = hashlib.sha256(slug.encode('utf-8')).hexdigest()
    time.sleep(1)
    return (slug, salt)

file = open("filiados_janeiro_2023.csv", "r",  encoding="utf8")

insert = "INSERT INTO socios (np, nome, sobrenome, slug, salt, status) VALUES "

while(True):
    try:
        linha   = file.readline()
        result  = re.findall("(\d{4,})[^\w]*([\w\s]+)", linha)
        print(result)
        nomeful = result[0][1].split(' ')
        nome    = nomeful.pop(0).capitalize()
        sobrenm = ' '.join(nomeful)
        slgslt  = generateSlugAndSalt(sobrenm)
        insert += "('"+result[0][0]+"', '"+nome+"', '"+sobrenm+"', '"+slgslt[0]+"', '"+slgslt[1]+"', 3),"
    except:
        break
    
insert = insert[0:-1]

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
cursor.execute(insert)
conn.commit()
conn.close()
