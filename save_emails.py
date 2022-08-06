import mariadb
import sys
import re 
from Config import Config 

def getEmails():
    file = open("emails.txt", "r")
    content = file.read() 
    return re.findall("(([^@;]+)<([^\s>;]+)([>\r;\n]|$))", content.replace("'", ''))

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
list = getEmails()
insrt = "INSERT INTO mailing (nome, sobrenome, email) VALUES (?,?,?) "

finalList = []
repetidos = 0

for item in list:
    fullnome = item[1].strip().split(" ", 1)
    nome = fullnome[0]
    sobrenome = fullnome[1]
    email = item[2]
    try:
        cursor.execute(insrt, (nome, sobrenome, email))
    except mariadb.Error as e:
        repetidos += 1 

conn.commit()
conn.close()

totalInseridos = len(list) - repetidos
print("Total Inseridos: "+str(totalInseridos))
print("Repetidos: "+str(repetidos))


