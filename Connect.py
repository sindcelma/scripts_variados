from Config import Config
import mariadb
import sys

class Connect:

    def __init__(self):
        try:
            config = Config().vars
            self.conn = mariadb.connect(
                user=config['user'],
                password=config['password'],
                host=config['host'],
                port=config['port'],
                database=config['database']
            )
        except mariadb.Error as e:
            print(f"Error to connect {e}")
            sys.exit(1)
    
    def get(self):
        return self.conn
