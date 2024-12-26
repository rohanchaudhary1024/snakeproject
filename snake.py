class Snake:
    '''
    Creates a snake where the head is at coordinate x, y and headed in
    direction given. The body is then automatically created behind the
    head.


    '''
    
    def __init__(self, x: int, y: int, length: int, direction: str): # Initializes Snake Object (V)
        self.direction = direction
        self.length = length
        self.body = []  
        for i in range(length):
            if direction == 'up':
                self.body.append((x,y+i))
            elif direction == 'down':
                self.body.append((x,y-i))
            elif direction == 'left':
                self.body.append((x+i,y))
            elif direction == 'right':
                self.body.append((x-i,y))

    # Useful Methods (Built-In)

    def __str__(self): # Print Format (V)
        return f"Snake moving {self.direction} of length {self.length}: {self.body}"

    def setBody(self, body) -> None: # Updates Body Variable (V)
        self.body = body

    def getBody(self): # Returns body list of coordinates (V)
        return self.body
    
    # Add required methods and others you may find useful below
    
    def step(self,direction): # Moves Snake, Applies Growth (V)
        if direction != None:
            self.direction = direction
        if self.direction == 'up':
            newHead = (self.body[0][0],self.body[0][1]-1)
            self.body.insert(0,newHead)
            if len(self.body) > self.length:
                self.body.pop()
        elif self.direction == 'down':
            newHead = (self.body[0][0],self.body[0][1]+1)
            self.body.insert(0,newHead)
            if len(self.body) > self.length:
                self.body.pop()
        elif self.direction == 'left':
            newHead = (self.body[0][0]-1,self.body[0][1])
            self.body.insert(0,newHead)
            if len(self.body) > self.length:
                self.body.pop()
        elif self.direction == 'right':
            newHead = (self.body[0][0]+1,self.body[0][1])
            self.body.insert(0,newHead)
            if len(self.body) > self.length:
                self.body.pop()
    
    
    def getHead(self): # Returns head coordinates (V)
        return(self.body[0])
    
    def getBody(self): # Returns body list (V)
        return(self.body)

    def getDirection(self): # Returns current direction (V)
        return(self.direction)
    
    def grow(self,amount): # Modifies Length (V)
        self.length += amount
    
    def isIntersecting(self,p1): # Given a point, checks if it intersects (V) 
        for i in range(len(self.body)):
            if p1 == self.body[i]:
                return(True)
        return(False)

