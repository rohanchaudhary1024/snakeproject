from ui import UI
from snake import Snake
from snakedata import SnakeData
from snakePlayer import SnakePlayer
class SnakeUI(UI):

    def __init__(self): # Initializes  (V)
        super().__init__()
        self.c1 = ("","")
        self.c2 = ("","")
        # add any state variables you want here...

    def drawFood (self,location): # Draw Food (V)
        self.writeCh("F",location[0],location[1])

    def drawSnakes(self,snakes): # Draw Snakes (V)
        for i in snakes:
            for j in range(len(snakes[0].body)):
                if ((snakes[0].body[j] == snakes[0].body[0]) or (snakes[0].body[j] == snakes[1].body[0])) and j != 0:
                    pass
                elif j == 0 and snakes[0].body[0] == snakes[1].body[0]:
                    self.writeCh("#",snakes[0].body[j][0],snakes[0].body[j][1])
                elif j == 0:
                    self.writeCh(self.c1[0],snakes[0].body[j][0],snakes[0].body[j][1])
                else:
                    self.writeCh(self.c1[1],snakes[0].body[j][0],snakes[0].body[j][1])
            for j in range(len(snakes[1].body)):
                if ((snakes[1].body[j] == snakes[0].body[0]) or (snakes[1].body[j] == snakes[1].body[0])) and j != 0:
                    pass
                elif j == 0 and snakes[1].body[0] == snakes[0].body[0]:
                    self.writeCh("#",snakes[1].body[j][0],snakes[1].body[j][1])
                elif j == 0:
                    self.writeCh(self.c2[0],snakes[1].body[j][0],snakes[1].body[j][1])
                else:
                    
                    self.writeCh(self.c2[1],snakes[1].body[j][0],snakes[1].body[j][1])
    
    def setSnakeCh(self,playerNum,snakeCharacters): # Assign Snake characters (V)
        if playerNum == 1:
            self.c1 = snakeCharacters
        else:
            self.c2 = snakeCharacters

    def getSnakeCh(self,playerNum): # Get stored Snake characters (V)
        if playerNum == 1:
            return(self.c1)
        else:
            return(self.c2)
    
ui = SnakeUI()

ui.setSnakeCh(1, ('A', 'a'))
ui.setSnakeCh(2, ('B', 'b'))
alex = SnakePlayer("Alex", 5, 10, 4, 'right')
bob = SnakePlayer("Bob", 35, 10, 4, 'left')
ui.drawFood((3, 5))
ui.drawSnakes([alex.getSnake(), bob.getSnake()])