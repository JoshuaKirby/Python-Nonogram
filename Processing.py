'''
Created on Jan 6, 2017

@author: Josh
'''
from PIL import Image

def boardProcess(image_path,block_size):
    #Does all required image processing in one line
    image = _crop(_compress(Image.open(image_path),block_size),block_size)
    x,y = image.size
    #Processes the compressed image into values
    board = _index(image,block_size)
    
    return x,y,board


def _compress(image_file,block_size):
    #converts the given image to B&W
    image_file = image_file.convert("1")
    
    xsize,ysize = image_file.size
    xsize = xsize - (xsize % block_size)
    ysize = ysize - (ysize % block_size)
    
    box = (0,0,xsize,ysize)
    
    image_file = image_file.crop(box)
    
    xLeft = 0
    x = 0
    y = block_size
    yRight = block_size
    
    while x < ysize:
        xLeft = 0
        yRight = block_size
        
        while xLeft < xsize:
            box = (xLeft,x,yRight,y)
            region = image_file.crop(box)
            total = 0
            
            for pixel in region.getdata():
                total = total + pixel
            colour = int(total/(block_size * block_size))
            if colour < (255/2):
                image_file.paste(0,box)
            else:
                image_file.paste(255,box)
                
            xLeft = xLeft + block_size
            yRight = yRight + block_size
            
        x = x + block_size
        y = y + block_size
        
    return image_file

def _crop(image_file,block_size):
    xsize,ysize = image_file.size
    
    x = 0
    y = block_size
    xLeft = 0
    yRight = block_size
    
    top = xsize
    bottom = 0
    left = ysize
    right = 0
    
    while x < ysize:
        xLeft = 0
        yRight = block_size
        
        while xLeft < xsize:
            box = (xLeft,x,yRight,y)
            region = image_file.crop(box)
            
            pixel = region.getdata()
            
            if pixel[0] != 255:
                if xLeft < left:
                    left = xLeft
                if x < top:
                    top = x
                if yRight > right:
                    right = yRight
                if y > bottom:
                    bottom = y
            
            xLeft = xLeft + block_size
            yRight = yRight + block_size
        
        x = x + block_size
        y = y + block_size
    
    image_file = image_file.crop((left,top,right,bottom))
    return image_file
    
def _index(image_file,block_size):
    board = []
    index = 0
    xsize,ysize = image_file.size
    for i in range(int((xsize / block_size) * (ysize / block_size))):
        board = board + [0]
    x = 0
    y = block_size
    xLeft = 0
    yRight = block_size
    
    while x < ysize:
        xLeft = 0
        yRight = block_size
        
        while xLeft < xsize:
            box = (xLeft,x,yRight,y)
            region = image_file.crop(box)
            
            pixel = region.getdata()
            
            if pixel[0] != 255:
                board[index] = 1
                
                
            
            xLeft = xLeft + block_size
            yRight = yRight + block_size
            index = index + 1
            
        x = x + block_size
        y = y + block_size
    
    return board
    
    
    
    
    
    
    
    
    
    
    
    pass
