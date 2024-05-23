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
            temp = reader['board']['boardconstants']
            self.put('boardconstants',temp)
            temp = reader['board']['jsonfilename']
            self.put('jsonfilename',temp)
            temp = reader['board']['kind']
            self.put('board',temp)
            temp = reader['board']['port']
            self.put('port',temp)
            temp = reader['board']['timeout']
            self.put('timeout',int(temp))
            temp = reader['board']['applicationport']
            self.put('applicationport',int(temp))
            temp = reader['board']['baudrate']
            self.put('baudrate',int(temp))
        except Exception as s:
            print(s)

    def __str__(self):
        return str(self.board)