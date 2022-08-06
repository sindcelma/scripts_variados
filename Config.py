import json
from SingletonMeta import SingletonMeta

class Config(metaclass=SingletonMeta):

    def __init__(self):
        try:
            f = open("config.json", "r")
            self.vars = json.loads(f.read())
        except:
            print("File 'config.json' dont exists")