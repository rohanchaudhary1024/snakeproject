from gamedata import GameData
from snakePlayer import SnakePlayer
from snake import Snake
import random
import math

class SnakeData(GameData):
    '''
    Holds all the key data associated with the snake game
    The players, the food, the score, the snakes, etc.
    '''

    def __init__(self): # Initializes datatable with food at (0,0) (V)
        super().__init__()
        self.setData('food', (0, 0))

    def setFood(self, loc) -> None: # Sets food (V)
        self.setData('food', loc)

    # add the required methods and any other you find useful

    def setPlayer(self,playernum,player): # Sets player in database (V)
        self.setData(str(playernum),player)

    def getPlayer(self,playernum): # Fetches player given playernum (V)
        return(self.getData(str(playernum)))

    def getSnake(self,playernum): # Fetches snake given playernum (V)
        return(self.getData(str(playernum)).s)
    
    def getFood(self): # Fetches food (V)
        return(self.getData('food'))

    def placeFoodFairly(self,width,height): # Places food 'fairly' (see standards in project) (V)
        p1 = self.getPlayer(1)
        p2 = self.getPlayer(2)
        pointLst = []
        for i in range(1,width+1,1):
            for j in range(1,height+1,1):
                isC = True
                point = (i,j)
                manhat1 = (abs(p1.s.body[0][0] - i))+ abs((p1.s.body[0][1] - j))
                manhat2 = (abs(p2.s.body[0][0] - i))+ abs((p2.s.body[0][1] - j))
                if abs(manhat2 - manhat1) < 3:
                    # print(point,manhat1,manhat2)
                    for k in (p1.s.body):
                        if point == k:
                            isC = False
                    for k in (p2.s.body):
                        if point == k:
                            isC = False
                    if isC == True:
                        pointLst.append(point)
        # for i in pointLst:
            # print(i)
        randInd = random.randrange(0,len(pointLst),1)
        # print("Chose")
        self.setFood(pointLst[randInd])

    def calculateBestMove(self,snakeNum,ui): # Singleplayer AI
        p1 = self.getPlayer(1)
        p2 = self.getPlayer(2)
        s1 = p1.getSnake()
        s2 = p2.getSnake()
        s1Body = s1.getBody()
        s2Body = s2.getBody()
        s2Head = s2Body[0]
        fLoc = self.getFood()

        possMoves = {
            "up": (s2Body[0][0],s2Body[0][1]-1),
            "down": (s2Body[0][0], s2Body[0][1]+1),
            "left": (s2Body[0][0]-1, s2Body[0][1]),
            "right": (s2Body[0][0]+1, s2Body[0][1])
        }
        chosMoves = {
            
        }
        for i in possMoves: # Iterate through possible moves
            isGood = True
            for j in range(len(s2Body)): # Check self collision
                if possMoves[i] == s2Body[j]:
                    isGood = False
                    #ui.writeMsg(i+"COL_S")
            for j in range(len(s1Body)): # Check collision with others
                if possMoves[i] == s1Body[j]:
                    isGood = False
                    #ui.writeMsg(i+"COL_O")
            if (possMoves[i][0] <= 0 or possMoves[i][0] > 40): # Check for out of bound x axis
                isGood = False
                #ui.writeMsg(i+"OOB_X")
            if (possMoves[i][1] <= 0 or possMoves[i][1] > 20): # Check for out of bound y axis
                isGood = False
                #ui.writeMsg(i+"OOB_Y")
            if (isGood == True):
                chosMoves.update({i:possMoves[i]})
        
        maxVal = 20000
        maxInd = None
        if len(chosMoves) == 0:
            return(None)
        elif len(chosMoves) == 0:
            for i in chosMoves:
                #ui.writeMsg(i+"OP_1")
                return(i)
        else:
            for i in chosMoves:
                manhat = (abs(chosMoves[i][0] - fLoc[0]) + abs(chosMoves[i][1]- fLoc[1]))
                #ui.writeMsg(i+str(manhat))
                if manhat < maxVal:
                    maxVal = manhat
                    maxInd = i

            #ui.writeMsg(maxInd+"CLOS")
            return(maxInd)
        
             
    def resetSnakes(self): # Resets Position of Snakes to Original (V)
        p1 = self.getPlayer(1)
        p2 = self.getPlayer(2)
        p1.resetSnake()
        p2.resetSnake()

