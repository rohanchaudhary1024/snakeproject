class GameData:

    def __init__(self):
        self.dbase = {}

    def setData(self, name: str, initValue: any):
        self.dbase[name] = initValue

    def getData(self, name: str):
        if name in self.dbase: 
            return self.dbase[name]
        else:
            return None

    def isData(self, name: str, value: any):
        if name in self.dbase:
            return self.dbase[name] == value
        else:
            return False
