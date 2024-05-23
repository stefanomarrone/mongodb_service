from src.utils.metaclasses import Singleton
from configparser import ConfigParser

class Configuration(metaclass=Singleton):

    def __init__(self):
        pass

    def __init__(self, inifilename):
        self.board = dict()
        self.load(inifilename)

    def get(self, key):
        return self.board[key]

    def put(self, key, value):
        self.board[key] = value

    def load(self,inifile):
        reader = ConfigParser()
        try:
            reader.read(inifile)
            temp = reader['server']['product_dbname']
            self.put('product',temp)
            temp = reader['server']['model_dbname']
            self.put('model',temp)
            temp = reader['server']['applicationport']
            self.put('applicationport',int(temp))
        except Exception as s:
            print(s)

    def __str__(self):
        return str(self.board)