import requests
import mariadb
import sys
import re 
from Config import Config 

from os import listdir
from os.path import isfile, join

directory = 'cct_itens'
onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
cct_id    = 1


url_image = 'http://www.assetsindcelma.com.br/images/cct/'


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

def genItem(item):
    file = open(directory+'/'+item, encoding='utf-8')
    cont = file.read()
    prts = cont.split('<br>')
    return (prts[0], prts[1][1:], prts[2][1:])

cursor = conn.cursor()
insert = "INSERT INTO cct_item (cct_id, imagem, item, resumo, texto) VALUES ("+str(cct_id)+",?,?,?,?) "

for item in onlyfiles:
    itm    = genItem(item)
    titulo = item[0:-4]
    commnt = itm[0]
    imagem = url_image+itm[1]
    texto  = itm[2]
    try:
        cursor.execute(insert, (imagem, titulo, commnt, texto))
    except mariadb.Error as e:
        print(e)
        break

conn.commit()
conn.close()