'''
Created on Jan 6, 2017
@author: Joshua Kirby
'''
import Game as gm
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import tkinter as tk
import pickle
from PIL import Image, ImageTk, ImageDraw
from _overlapped import NULL
from Game import Game
import webbrowser

#TODO:
# Hint UI

#Globals

BLOCKSIZE = 50
IMAGE_SIZE = 10
correct = Image.new("1",(IMAGE_SIZE,IMAGE_SIZE),0)
default = Image.new("1",(IMAGE_SIZE,IMAGE_SIZE),255)
incorrect = Image.new("RGB",(1,1))
root = tk.Tk()
game_over = False
gamenum = 0
game = 0

def incorrectImage():
    # This function generates a red X image and stores it in incorrect
    global IMAGE_SIZE,incorrect
    
    incorrect = Image.new("RGB",(IMAGE_SIZE,IMAGE_SIZE),(255,255,255))
    
    draw = ImageDraw.Draw(incorrect)
    
    draw.line((0,0) + incorrect.size, fill=(255,0,0))
    draw.line((0,incorrect.size[1],incorrect.size[0],0),fill=(255,0,0))
    del draw

def main():
    global game,root
    global correct,incorrect,default,BLOCKSIZE,root
    #starts a random game
    game = gm.Game(NULL,BLOCKSIZE,True)
    #builds the board view
    board = buildBoard(root,game,BLOCKSIZE)
    board.pack()
    incorrectImage()
    mbar = buildMenu(root)
    root["menu"] = mbar
    
    tk.mainloop()

def buildBoard(parent,game,block_size):
    #default image for board setup
    photo = ImageTk.PhotoImage(default)
    #required to build the board of buttons
    outer = tk.Frame(parent,border=2,relief="sunken")
    inner = tk.Frame(outer)
    inner.pack()
    #gets size for looping
    x,y = game.getSize()
    #loop creates buttons with the default image for every index in game
    for rows in range(y):
        #print("r = " + str(rows))
        for cols in range(x):
            #print("c = " + str(cols))
            if(rows == 0):
                hint = tk.Label(inner,text=generate_label(game.getHints(cols,0),1))
                hint.grid(row=0, column=cols+1)
            
            cell = tk.Button(inner,image=photo)
            cell.configure(command=lambda r=rows,c=cols,cl=cell:evClick(r,c,game,cl))
            cell.image = photo
            cell.grid(row=rows+1,column=cols+1)
        hint = tk.Label(inner,text=generate_label(game.getHints(rows,1),0))
        hint.grid(row=rows+1,column=0)    
    #returns the grid of buttons
    return outer
def generate_label(text,orientation):
    output = ""
    if(orientation == 1):
        for val in range(len(text)):
            output = output + str(text[val]) + "\n"
    if(orientation == 0):
        for val in range(len(text)):
            output = output + str(text[val]) + " "
    #print(output)
    return output

def buildMenu(parent):
    menus = (
        ("File", ( ("New", evNew),
                   ("Resume", evResume),
                   ("Save", evSave),
                   ("Exit", evExit))),
        ("Help",( ("Help", evHelp),
                  ("About", evAbout)))
    )
    
    menubar = tk.Menu(parent)
    for menu in menus:
        m = tk.Menu(parent)
        for item in menu[1]:
            m.add_command(label=item[0],command=item[1])
        menubar.add_cascade(label=menu[0],menu=m)
    return menubar
    
def update(row,col,cell,cell_value):
    global correct,incorrect
    #images to change to
    pCorrect = ImageTk.PhotoImage(correct)
    pIncorrect = ImageTk.PhotoImage(incorrect) 
    #changes the image based on the click value (managed in game object)
    if cell_value == 1:
        cell.configure(image=pCorrect)
        cell.image = pCorrect
    if cell_value == 0:
        cell.configure(image=pIncorrect)
        cell.image = pIncorrect

def dummy():
    mb.showinfo("Dummy","This is missing functionality! Let me know what you hit to find this!")
    
    
def evClick(row,col,game,cell):
    global root,BLOCKSIZE,game_over
    #checks the validity if the move 
    #if game_over:
    #    return
    result = game.checkMove(row,col)
    #"D" means Dead out of lives 
    if result == "D":
        update(row,col,cell,0)
        mb.showerror("Game over","OUT OF LIVES")
        game_over = True
    #"C" means correct
    elif result == "C":
        update(row,col,cell,1)
    #"I" means incorrect
    elif result == "I":
        update(row,col,cell,0)
    elif result == "W":
        update(row,col,cell,1)
        mb.showerror("Game over","You Win!")
        game_over = True
    return
    
    
def evNew():
    global game,root,game_over,gamenum
    answer = mb.askyesnocancel("Image Select", "Would you like to start a new game with an image?") 
    
    if(answer == True):
        game = gm.Game(fd.askopenfilename(),BLOCKSIZE,False)
    elif(answer == None):
        return
    else:
        game = gm.Game(NULL,BLOCKSIZE,True)
        
    game_over = False
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()
    board = buildBoard(root,game,BLOCKSIZE)
    board.pack()
    #print(root.children)
    gamenum = gamenum + 1
    return

def evResume():
    global game,root
    with open('save.pkl','rb') as save_in:
        game = pickle.load(save_in)
        
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()
    board = buildBoard(root,game,BLOCKSIZE)
    board.pack()
    
    board = game.getBoard()
    check = game.getTried()
    x,y = game.getSize()
    for widget in root.children.values(): # get the widgets in root
        #print(widget)
        if isinstance(widget, tk.Frame): # find the frame (outer)
            #print("Hi")
            for inner in widget.children.values():
                i = 0
                for cell in inner.children.values():
                    if isinstance(cell, tk.Button):
                        if(check[i] == 1):
                            update(int(i / x),(i % x),cell,board[i])
                        i = i + 1
    
def evSave():
    global Game
    with open('save.pkl','wb') as output:
        pickle.dump(game,output,-1)
    
def evAbout():
    mb.showinfo("About","Python Nonogram created by Joshua Kirby\nContact me at Joshua.Kirby@outlook.com")
    
def evExit():
    if(mb.askokcancel("Quit","Would you like to quit?")):
        if(mb.askokcancel("Save","Would you like to save before you quit?")):
            evSave()
        root.quit()
    return

def evHelp():
    webbrowser.open("http://www.puzzlemadness.co.uk/rules/nonograms/",new=0, autoraise=True)
    
if __name__ == '__main__':
    main()