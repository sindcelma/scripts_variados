import json
from SingletonMeta import SingletonMeta

class Config(metaclass=SingletonMeta):

    def __init__(self, dev=False):
        file = 'config.json'
        if dev:
            file = 'config.dev.json'
        try:
            f = open(file, "r")
            self.vars = json.loads(f.read())
        except:
            print("File '"+file+"' dont exists")