from ui import UI
import curses
from snake import Snake
from snakedata import SnakeData
from snakePlayer import SnakePlayer
from snakeui import SnakeUI
import time
'''
Just a place to try out some code
'''

def main(stdscr):
    gameUI = SnakeUI()

    gameUI.writeMsg("Hello World!!")
    gameUI.drawFood((3, 5))
    gameUI.setSnakeCh(1, ('A', 'a'))
    gameUI.setSnakeCh(2,('B','b'))
    alex = SnakePlayer("Alex", 5, 10, 4, 'right')
    bob = SnakePlayer("Bob", 5, 12, 4, 'up')
    s1 = alex.getSnake()
    s2 = bob.getSnake()
    s1Body = s1.getBody()
    s2Body = s2.getBody()
    s1Head = s1.getHead()
    s2Head = s2.getHead()
    data = SnakeData()
    data.setPlayer(1,alex)
    data.setPlayer(2,bob)
    data.setFood((4,12))

    for i in range(10):
        s1.step(None)
        s2.step(None)
        
        s2Head = s2.getHead()
        gameUI.clearGameWindow()
        gameUI.drawFood((4,12))
        gameUI.drawSnakes([alex.getSnake(), bob.getSnake()])
        gameUI.updateGameWindow()
        gameUI.writeMsg(str(s1Body))
        gameUI.writeMsg(str(s2Head))
        for i in range(0,len(s1Body)): # Checks for other-collision
            if s1Body[i] == s2Head:
                gameUI.writeMsg("3")
        time.sleep(5)
    

curses.wrapper(main)

