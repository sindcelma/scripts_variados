import requests
import json
from Config import Config
import time
from Connect import Connect

config = Config().vars
totalPages = 49
currentPage = 1

url = 'https://emailmarketing.locaweb.com.br/api/v1/accounts/'+config['accid']+"/contacts"

headers = {
    'Content-Type': 'application/json',
    'X-Auth-Token': config['acckey']
}



itens  = []

while currentPage <= totalPages:
    response = requests.get(url+"?page="+str(currentPage), headers=headers)
    time.sleep(2)
    currentPage += 1
    for it in json.loads(response.text)['items']:
        print(it)
        itens.append(it)

try:
    conn   = Connect().get()
    cursor = conn.cursor()
    for item in itens:
        cursor.execute("UPDATE mailing SET loc_id = %s WHERE email LIKE %s", (str(item['id']), str(item['email'])))
    conn.commit()
    conn.close()
except:
    print("Erro ao tentar editar contar.")


print("Script Finalizado.")