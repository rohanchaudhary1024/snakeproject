from player import Player
from snake import Snake

class SnakePlayer(Player):
    '''
    Creates a Player with a Snake where the head is at coordinate x, y and headed in
    direction given. The body is then automatically created behind the
    head.
    '''

    def __init__(self, name: str, x: int, y: int, length: int, direction: int): # Initializes Player w/ Snake and Name (V)
        super().__init__(name)
        self.x = x
        self.y = y
        self.length = length
        self.direction = direction
        self.s = Snake(x,y,length,direction)

    def getSnake(self): # Returns Player Snake (V)
        return(self.s)
    
    def getHead(self): # Returns Snake Head (V)
        return(self.s.getBody()[0])
    
    def getScore(self): # Returns Score (V)
        return(self.score)

    def addScore(self,amount): # Edits Score (V)
        self.score += amount

    def getName(self): # Returns Name (V)
        return(self.name)
    
    def resetSnake(self): # Resets position of One Snake (V)
        self.s = Snake(self.x,self.y,self.length,self.direction)


    
