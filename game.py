# Copyright Rohan Chaudhary, chaudhary2rohan@gmail.com, circa 2-17-24
# FINAL SUBMISSION (WITH) (AI BREAKS TEST CASES  (ONE IN SPECIFIC) ) FOR BASIC FUNCTIONALITY PLEASE LOOK AT PRIOR SUB
from snake import Snake
from snakePlayer import SnakePlayer
from snakedata import SnakeData
from snakeui import SnakeUI
import curses
import time

def moveSnakes(ui: SnakeUI, data: SnakeData):
    # Snake Movement
    p1 = data.getPlayer(1)
    p2 = data.getPlayer(2)
    p1Name = p1.getName()
    p2Name = p2.getName()
    s1 = p1.getSnake()
    s1Head = s1.getHead()
    s1Body = s1.getBody()
    s2 = p2.getSnake()
    s2Head = s2.getHead()
    s2Body = s2.getBody()
    foodCoord = data.getFood()
    
    p1Input = ui.getPlayerMove(1)
    s1.step(p1Input)
    if data.getData("gm")  == "basic":
        p2Input = ui.getPlayerMove(2)
    else:
        p2Input = data.calculateBestMove(2,ui)

    s2.step(p2Input)
    s1Head = s1.getHead()
    s2Head = s2.getHead()
    s1Body = s1.getBody()
    s2Body = s2.getBody()
    # Initial Display
    ui.clearGameWindow()
    ui.drawFood(foodCoord)
    ui.drawSnakes([s1,s2])
    ui.updateGameWindow()

    # Status Code Check
    status = [0,0]

    if (s1Head[0] < 1 or s1Head[0] > 40) or (s1Head[1] < 1 or s1Head[1] > 20): # Checks if S1 is OOB
        status[0] = 1
        ui.writeMsg("{p1} went Out of Bounds.".format(p1=p1Name))
    else:
        for i in range(1,len(s1Body)): # Checks for self-collision
            if s1Body[i] == s1Head:
                status[0] = 2
                ui.writeMsg("{p1} self-collision.".format(p1=p1Name))
        for i in range(0,len(s2Body)): # Checks for other-collision
            if s2Body[i] == s1Head:
                status[0] = 3
                ui.writeMsg("{p1} collided into {p2}".format(p1=p1Name,p2=p2Name))
        if status[0] != 2 or status[0] != 3: # Checks for food
            if s1Head == foodCoord:
                status[0] = 4
                data.placeFoodFairly(40,20)
                p1.addScore(1)
                s1.grow(1)
                ui.writeScore(1, p1.getScore())
                
    
    if (s2Head[0] < 1 or s2Head[0] > 40) or (s2Head[1] < 1 or s2Head[1] > 20): # Checks if S2 is OOB
        status[1] = 1
        ui.writeMsg("{p2} went Out of Bounds.".format(p2=p2Name))

    else:
        for i in range(1,len(s2Body),1): # Checks for self-collision
            if s2Body[i] == s2Head:
                status[1] = 2
                ui.writeMsg("{p2} self-collision.".format(p2=p2Name))
        for i in range(0,len(s1Body)): # Checks for other-collision
            if s1Body[i] == s2Head:
                status[1] = 3
                ui.writeMsg("{p2} collided into {p1}".format(p2=p2Name,p1=p1Name))
        if status[1] != 2 or status[1] != 3: # Checks for food
            if s2Head == foodCoord:
                status[1] = 4
                data.placeFoodFairly(40,20)
                p2.addScore(1)
                s2.grow(1)
                ui.writeScore(2, p2.getScore())
    
    return(status)
def playSnake(ui: SnakeUI, data: SnakeData,d):
    # Var Init
    speed = .5
    if d == "1":
        pass
    elif d == "2":
        speed = .25
    elif d == "3":
        speed = .1
    p1 = data.getPlayer(1)
    p2 = data.getPlayer(2)
    s1 = p1.getSnake()
    s1Head = s1.getHead()
    s1Body = s1.getBody()
    s2 = p2.getSnake()
    s2Head = s2.getHead()
    s2Body = s2.getBody()
    foodCoord = data.getFood()
    # Places food fairly
    data.placeFoodFairly(40,20)

    # Loop moveSnakes
    gameOver = False
    while gameOver == False:
        status = moveSnakes(ui,data)
        if status[0] == 1 or status[0] == 2 or status[0] == 3 or status[1] == 1 or status[1] == 2 or status[1] == 3:
            ui.writeMsg("Game Over.")
            gameOver = True
        
        ui.wait(speed)
    
    # Update Scores
    if (status[0] == 1 or status[0] == 2 or status[0] == 3) and (status[1] == 1 or status[1] == 2 or status[1] == 3):
        ui.writeMsg("Both Players died at the same time - No Score Awarded.")
    elif (status[0] == 1 or status[0] == 2 or status[0] == 3):
        p2.addScore(5)
        ui.writeScore(2, p2.getScore())
    elif (status[1] == 1 or status[1] == 2 or status[1] == 3):
        p1.addScore(5)
        ui.writeScore(1, p1.getScore())
    

        
            

def main(stdscr):
    data = SnakeData()
    data.setData('mode', 'basic')
    data.setData('numplayers', 2)

    ui = SnakeUI()
    ui.resetWindows()
    ui.setPlayerKeyMap(1, [('w', 'up'), ('a', 'left'), ('s', 'down'), ('d', 'right')] )
    ui.setPlayerKeyMap(2, [('i', 'up'), ('j', 'left'), ('k', 'down'), ('l', 'right')] )
    ui.setSnakeCh(1, ('X', 'x')) 
    ui.setSnakeCh(2, ('O', 'o'))
    isBasic = False
    basicAns = ui.askMsg("Do you want to play the basic version of snake? (y/n)")
    if basicAns == "y":
        isBasic = True
    
    ui.clearMsgWindow()
    ui.writeMsg("Let's play Snake!!!")

    # you can delete this but it waits for a key before the program continues...
    ui.waitForKey()

    # Get player names, make SnakePlayers, add to GameData, say Hi!
    if isBasic == False:
        gMode = ui.askMsg("Gamemode? (Basic, 1P)")
        if gMode == "1P":
            data.setData("gm","1P")
        else:
            data.setData("gm","basic")
        diff = ui.askMsg("Choose a Difficulty. (1-3, 3 is Hardest)")
    else:
        diff = 1
        data.setData("gm","basic")
    p1Name = ui.askMsg("Player 1: What is your name?")
    ui.writeMsg("Hi {name}".format(name=p1Name))
    p1 = SnakePlayer(p1Name,5,10,4,'right')
    data.setPlayer(1,p1)
    if data.getData("gm") == "1P":
        pass
        p2Name = "AI"
    else:
        p2Name = ui.askMsg("Player 2: What is your name?")
        ui.writeMsg("Hi {name}".format(name=p2Name))
    p2 = SnakePlayer(p2Name,36,10,4,'left')
    data.setPlayer(1,p1)
    data.setPlayer(2,p2)

    # Write out scores and name to Header window
    ui.writePlayerNames(p1Name,p2Name)
    ui.writeScore(1,0)
    ui.writeScore(2,0)
    
    gameOver = False
    while gameOver == False:
        playSnake(ui,data,diff)
        ans = ui.askMsg("Do you want to play snake again? (y/n)")
        if ans != "y" and ans != "yes":
            gameOver = True
        else:
            p1.resetSnake()
            p2.resetSnake()
            ui.resetWindows()
            ui.writeScore(1, p1.getScore())
            ui.writeScore(2, p2.getScore())





if __name__ == "__main__":      # DO NOT DELETE
    curses.wrapper(main)        # DO NOT DELETE
