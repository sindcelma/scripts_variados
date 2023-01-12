import mariadb
import sys
from Config import Config 
from hashlib import sha256
import time


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


insert = "INSERT INTO socios (nome, sobrenome, np, cpf, slug, salt, status) VALUES (?,?,?,?,?,?,?) "
cursor = conn.cursor()

file  = open("socios_temp.txt", "r", encoding="utf-8")
value = file.read()
parts = value.split("#")
nomes = parts[0].split("\n")
dados = parts[1].split("\n")

print(dados)

i = 0
while i < len(dados):

    try:
        
        if(dados[i] == ""):
            i+=1; continue

        nomesParts = nomes[i].split(" ", 1)
        dadosParts = dados[i].split(" ")

        if(len(nomesParts) < 2):
            i+=1; continue
        print(dadosParts[0])
        nome = nomesParts[0]
        sobr = nomesParts[1]
        np   = int(dadosParts[0].strip())
        cpf  = dadosParts[1]
        slug = sha256((cpf).encode('utf-8')).hexdigest()
        salt = sha256((slug+"slug").encode('utf-8')).hexdigest()
        stat = 3

        cursor.execute(insert, (nome, sobr, np, cpf, slug, salt, stat))
    
    except:
        print("aqui...");

    i += 1
    

conn.commit()
conn.close()
