'''
Created on Jan 6, 2017

@author: Josh
'''
import Processing as pc
import random 
import math

#TODO
# Win checking



class Game(object):
    '''
    classdocs
    '''
    _DEBUG_RANDOM_GEN = 25 # Side length squared
    x = 0
    y = 0
    board = []
    tried = []
    lives = 5
    hints = []
    blocksize = 0
    
    def __init__(self,image_path,block_size,randstart):
        '''
        Constructor
        '''
        
        if(randstart):
            for i in range(self._DEBUG_RANDOM_GEN):
                self.board = self.board + [random.randint(0,1)]
                self.x = int(math.sqrt(self._DEBUG_RANDOM_GEN))
                self.y = int(math.sqrt(self._DEBUG_RANDOM_GEN))
            
        else:
            #Processing builds the board from the image and returns it
            self.x,self.y,self.board = pc.boardProcess(image_path,block_size)
            #correcting for the board size vs image size
            self.x = int(self.x/block_size)
            self.y = int(self.y/block_size)
            #creates a list to hold player guesses so they cant miss click
        for i in range(self.x * self.y):
            self.tried = self.tried + [0]
            
        self._generate_Hints()
        #print(self.y)
        #print(self.hints)
        #print(len(self.hints) - self.x - self.y)
        
        
    def checkMove(self,inY,inX):
        #changes (X,Y) coord into index
        index = (inY * self.y) + inX
        #if stack to find correct or incorrect moves, do nothing if it has already been tried
        if (self.tried[index] == 1):
            return 
        if(self.board[index] == 1):
            self.tried[index] = 1
            if self._checkWin():
                return "W"
            return "C"
        if(self.board[index] == 0):
            self.tried[index] = 1
            self.lives = self.lives - 1
            if self.lives <= 0:
                return "D"
            return "I"
        
    def _generate_Hints(self):
        hintval = 0
        temp = []
        #gets hints for columns
        for col in range(self.x):
            for row in range(self.y):
                if(self.board[row*self.y + col] == 1):
                    hintval = hintval + 1
                if(self.board[row*self.y + col] == 0 and hintval > 0):
                    temp = temp + [hintval]   
                    hintval = 0
            if(hintval > 0):
                temp = temp + [hintval]
            hintval = 0
            
                
            self.hints = self.hints + [temp]
            temp = []
        temp = []
        #gets hints for rows
        for row in range(self.y):
            for col in range(self.x):
                if(self.board[row*self.y + col] == 1):
                    hintval = hintval + 1
                if(self.board[row*self.y + col] == 0 and hintval > 0):
                    temp = temp + [hintval]   
                    hintval = 0
            if(hintval > 0):
                temp = temp + [hintval]
            hintval = 0
            
            self.hints = self.hints + [temp] 
            temp = []      
        temp = []        
        #print(self.hints)
        '''this makes weird triangle hints, I'm saving it cause it's interesting and 
    I don't want to kill it by replacing it with the proper function'''
    def _generate_Hints_BAK(self):
        hintval = 0
        temp = []
        for val in range(self.x):
            for row in range(self.y):
                if(self.board[row*self.y + val] == 1):
                    hintval = hintval + 1
                if(self.board[row*self.y + val] == 0 and hintval > 0):
                    temp = temp + [hintval]   
                    hintval = 0
            temp = temp + [hintval]
            hintval = 0
            if(temp == []):
                temp = temp + [0]
            self.hints = self.hints + [temp]
        temp = []
        for row in range(self.y):
            for val in range(self.x):
                if(self.board[row*self.y + val] == 1):
                    hintval = hintval + 1
                if(self.board[row*self.y + val] == 0 and hintval > 0):
                    temp = temp + [hintval]   
                    hintval = 0
            temp = temp + [hintval]
            hintval = 0
            if(temp == []):
                temp = temp + [0]
            self.hints = self.hints + [temp]       
        temp = []        
    
    def _getHints(self,val,orientation):
        return self.hints[self.x*orientation + val]
    def getHints(self,val,orientation):
        #print(self.x,val)
        return self.hints[self.x*orientation + val]
    def _checkWin(self):
        out = True
        for i in range(self.x*self.y):
            if(self.board[i] == 1 and self.tried[i] != 1):
                out = False
        return out   
            
    def getLives(self):
        return self.lives
    
    def getBoard(self):
        return self.board
    def getTried(self):
        return self.tried
    def getSize(self):
        return self.x,self.y
        