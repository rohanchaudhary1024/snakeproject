class Player:
    '''
    A very generic Player class that might be used for an
    assortment of games.
    '''

    def __init__(self, name: str):
        self.name = name
        self.score = 0

    def getName(self) -> str:
        return self.name
    
    def setName(self, name: str) -> None:
        self.name = name

    def getScore(self) -> int:
        return self.score

    def updateScore(self, point: int) -> None:
        self.score += point


