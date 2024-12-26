import curses
import time

'''
DO NOT MODIFY
DO NOT MODIFY
DO NOT MODIFY
DO NOT MODIFY
DO NOT MODIFY
DO NOT MODIFY
'''

class UI:
    '''
    UI is a curses-based 3-paned window - a message window, a game window and a message window
    with methods to write to different windows on the screen
    ┌────────────────────────────────────────┐
    │ Header Window                          │
    ├────────────────────────────────────────┤
    │ Game Window                            │
    │                                        │
    │                                        │
    │                                        │
    │                                        │
    │                                        │
    │                                        │
    │                                        │
    │                                        │
    │                                        │
    │                                        │
    │                                        │
    │                                        │
    │                                        │
    │                                        │
    │                                        │
    │                                        │
    │                                        │
    │                                        │
    │                                        │
    ├────────────────────────────────────────┤
    │Message Window                          │
    │                                        │
    │                                        │
    │                                        │
    └────────────────────────────────────────┘
    '''
    WIDTH = 40
    HEADER_HEIGHT = 1
    GAME_HEIGHT = 20
    MSG_HEIGHT = 5

    # total height with the 4 horizontal border lines
    TOTAL_HEIGHT = GAME_HEIGHT + HEADER_HEIGHT + MSG_HEIGHT + 4

    # total width with the 2 vertical border lines
    TOTAL_WIDTH = WIDTH + 2

    def __init__(self):
        self.stdscr = curses.initscr()
        curses.curs_set(0)          # make cursor invisible
        self.stdscr.keypad(True)    # handle keypad
        self.stdscr.nodelay(1)      # make getch() non-blocking

        self.height, self.width = self.stdscr.getmaxyx()
        self.playerKeys = [ [], [] ]    # initialize for 2 players
        self.playerMoves = [ [], [] ]
        self.playerKeyDef = [ {}, {} ]

        # ask for a minimum size on the console before starting
        while self.height < self.TOTAL_HEIGHT or self.width < self.TOTAL_WIDTH:
            self.stdscr.addstr(0, 0, f"Please resize your console to at least {self.TOTAL_HEIGHT} wide and {self.TOTAL_WIDTH} tall")
            self.stdscr.addstr(1, 0, f"Console size is {self.width} x {self.height}")
            self.stdscr.getch()
            self.wait(0.2)
            self.stdscr.clear()
            self.height, self.width = self.stdscr.getmaxyx()
            self.stdscr.refresh()

        # make overall game window and the 3 sub-windows for header/game/message
        self.mainWindow = curses.newwin(self.TOTAL_HEIGHT, self.TOTAL_WIDTH, 0, 0)
        self.headerWindow = curses.newwin(self.HEADER_HEIGHT, self.WIDTH, 1, 1)
        self.gameWindow = curses.newwin(self.GAME_HEIGHT+2, self.TOTAL_WIDTH, self.HEADER_HEIGHT+1, 0)
        self.gameWindow.nodelay(1)
        self.msgWindow = curses.newwin(self.MSG_HEIGHT, self.WIDTH,
                self.TOTAL_HEIGHT-self.MSG_HEIGHT-1, 1)
        self.msgWindow.scrollok(True)
        
        self.mainWindow.border()
        self.mainWindow.refresh()

        # draw the game boarders with the Tee's so that it looks nice inside the game border
        self.gameBorder()          

        # special UI modes
        self.keyIn = None       # used for testing purposes
        self.pauseMode = False  # default
        self.testAnswerQ = None # default off

    def setPauseMode(self, mode: bool):
        '''
        Enables a pause modw where a space can be used to stop play
        '''
        self.pauseMode = mode

    def getHeight(self) -> int:
        '''
        Returns the height of the Game window
        '''
        return self.GAME_HEIGHT
    
    def getWidth(self) -> int:
        '''
        Returns the width of the Game window
        '''
        return self.WIDTH

    def getPlayerMove(self, playerNum: int) -> str:
        '''
        return the next move for 'playerNum'
        Uses the playerKeyDef map that maps a key press to a 
        move command string - like 'w' -> 'up'
        '''

        # Normal user key input - gather any key inputs into a player input Q
        p = playerNum - 1
        ch = self.gameWindow.getch(1,1)
        while ch != -1:

            # pause on ' ' 
            if self.pauseMode and chr(ch) == ' ':
                self.waitForKey()

            if chr(ch) in self.playerKeyDef[0]:
                move = self.playerKeyDef[0][chr(ch)]
                # ignore auto-repeat of a key press when a key is held down
                if len(self.playerMoves[0]) == 0 or move != self.playerMoves[0][-1]:
                    self.playerMoves[0].append(move)
            if chr(ch) in self.playerKeyDef[1]:
                move = self.playerKeyDef[1][chr(ch)]
                # ignore auto-repeat of a key press when a key is held down
                if len(self.playerMoves[1]) == 0 or move != self.playerMoves[1][-1]:
                    self.playerMoves[1].append(move)
            ch = self.gameWindow.getch(1,1)
        
        # get next player move from queue
        if len(self.playerMoves[p]) == 0:
            return None
        else:
            return self.playerMoves[p].pop(0)

    def getKey(self):
        return self.gameWindow.getch()

    def setPlayerKeyMap(self, playerNum: int, keyDefs: list[ tuple[str, str] ]):
        '''
        Define a set of key mappings for each player
        For example, [ ('q', 'quit'), ('w', 'up') ] defines two key mappings
        '''
        p = playerNum - 1
        for (key, what) in keyDefs:
            if key not in self.playerKeyDef[p]:
                self.playerKeyDef[p][key] = what

    def resetWindows(self):
        '''
        Clears out the Game and Message windows - keeps the header window the same
        '''
        self.gameBorder()
        self.clearMsgWindow()

    def clearMainWindow(self):
        self.mainWindow.clear()
        self.mainWindow.refresh()

    def clearHeaderWindow(self) -> None:
        self.headerWindow.clear()
        self.headerWindow.refresh()

    def clearGameWindow(self) -> None:
        self.clearRect(self.gameWindow, 1, 1, self.GAME_HEIGHT, self.WIDTH)

    def clearMsgWindow(self) -> None:
        self.msgWindow.clear()
        self.msgWindow.refresh()

    def clearRect(self, win, start_y, start_x, height, width):
        for y in range(start_y, start_y + height):
            win.addstr(y, start_x, ' ' * width)
        win.refresh()

    def gameBorder(self) -> None:
        self.gameWindow.border()
        maxX = self.gameWindow.getmaxyx()[1] - 1
        maxY = self.gameWindow.getmaxyx()[0] - 1
        self.gameWindow.addch(0, 0, curses.ACS_LTEE)
        self.gameWindow.addch(maxY, 0, curses.ACS_LTEE)
        self.gameWindow.addch(0, maxX, curses.ACS_RTEE)
        self.gameWindow.insch(maxY, maxX, curses.ACS_RTEE)
        self.gameWindow.refresh()

    def writeCh(self, ch: str, x: int, y: int) -> None:
        '''
        Writes a character (or string) to the gameWindow buffer at (x, y)
        It does not update the screen, so a updateGameWindow() call needs to
        be done to display it
        '''
        self.gameWindow.addstr(y, x, ch)

    def updateGameWindow(self) -> None:
        '''
        Draw the changes to the Game window made by writeCh()
        '''
        self.gameWindow.refresh()

    def wait(self, sec) -> None:
        time.sleep(sec)

    def waitForKey(self) -> None:
        while self.stdscr.getch() == -1:
            pass

    def writeHeaderMsg(self, text: str) -> None:
        '''
        Write the text message to the Header window
        '''
        self.headerWindow.addstr(text)
        self.headerWindow.refresh()

    def writeMsg(self, text: str) -> None:
        '''
        Write 'text' message to the message window.
        It will automatically add a \n and go to the next line of the message window
        The message window scrolls automatically
        '''
        self.msgWindow.addstr(text + '\n')
        self.msgWindow.refresh()

    def askMsg(self, prompt: str) -> str:
        '''
        Write out prompt to the Message window and wait for user to type in a response
        Return the response string

        Similar in use to the console's input() function but for this UI window framework
        '''

        # clear out the key presses before prompting
        while self.stdscr.getch() != -1:
            pass

        # Normal Mode
        self.msgWindow.addstr(prompt + " ")
        curses.curs_set(1)          # make cursor visible
        curses.echo()
        self.msgWindow.nodelay(0)   # wait for the <ENTER>

        userInput = self.msgWindow.getstr().decode('utf-8')

        curses.curs_set(0)          # make cursor invisible again
        curses.noecho()
        self.msgWindow.nodelay(1)

        return userInput

    def writePlayerNames(self, n1: str, n2: str) -> None:
        '''
        Write n1/n2 names to the Header window with spacing that allows for the score
        to be next to the names
        '''
        self.headerWindow.addstr(0, 5, n1)
        self.headerWindow.addstr(0, self.WIDTH - 5 - len(n2), n2)
        self.headerWindow.refresh()

    def writeScore(self, pNum: int, score: int) -> None:
        '''
        Write the score of player pNum in to the Header window
        Player 1 appears on the left and player 2 score appears on the right
        If the score is bigger than 999 it may not work...
        '''
        if pNum == 1:
            self.headerWindow.addstr(0, 1, str(score).rjust(3, " "))
        elif pNum == 2:
            self.headerWindow.addstr(0, self.WIDTH - 4, str(score).rjust(3, " "))
        self.headerWindow.refresh()

        

