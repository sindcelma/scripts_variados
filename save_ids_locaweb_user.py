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


conn = Connect().get()
cursor = conn.cursor()

while currentPage <= totalPages:
    response = requests.get(url+"?page="+str(currentPage), headers=headers)
    time.sleep(2)
    currentPage += 1
    items = json.loads(response.text)['items']
    for item in items:
        print(item)
        try:
            cursor.execute("UPDATE mailing SET loc_id = %s WHERE email LIKE %s", (str(item['id']), str(item['email'])))
        except:
            print("Erro ao tentar editar contar.")

conn.commit()
conn.close()