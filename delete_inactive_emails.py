import requests
import json
import time
from Config import Config
from Connect import Connect

config = Config().vars

url = 'https://emailmarketing.locaweb.com.br/api/v1/accounts/'+config['accid']+"/contacts"

headers = {
    'Content-Type': 'application/json',
    'X-Auth-Token': config['acckey']
}

conn = Connect().get()
cursor = conn.cursor()

totalPages = 6
currentPage = 1

while currentPage <= totalPages:
    response = requests.get(url+"?status=disabled&page="+str(currentPage), headers=headers)
    time.sleep(2)
    currentPage += 1
    items = json.loads(response.text)['items']
    
    for item in items:
        print(item)
        try:
            cursor.execute("UPDATE mailing SET ativo = ? WHERE email = ?", (2, str(item['email'])))
        except:
            print("Erro ao tentar alterar status da conta.")
        
conn.commit()
conn.close()
print("Processo finalizado.")