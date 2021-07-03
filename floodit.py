import pygame
from pygame import color
import os
from random import *
import time
# constants
CELL_DIM = 30
pygame.init();
pygame.font.init()
FONT = pygame.font.SysFont('Comic Sans MS', CELL_DIM * 2 // 3)

WIDTH, HEIGHT = 900, 500

pygame.display.set_caption("Flood-It")

# COLORS
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
WHITE = pygame.Color(255, 255, 255)
GREY = pygame.Color(210,210,210)
BLACK = pygame.Color(0,0,0)
DKGREY = pygame.Color(175,175,175)
# fps
FPS = 20


# button class
""" //----------- BUTTON ------------/// """
class Button:

    def __init__(self, x, y, w, h, text, color):
        self.x = x;
        self.y = y;
        self.w = w;
        self.h = h;
        self.color = color;
        self.text = text;

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x * CELL_DIM - 2, self.y * CELL_DIM - 2, self.w+4 * CELL_DIM, self.h * CELL_DIM + 4), 0)
        
        pygame.draw.rect(win, self.color, (self.x * CELL_DIM, self.y * CELL_DIM, self.w * CELL_DIM, self.h * CELL_DIM), 0)

        if self.text != '':
            text = FONT.render(self.text, 1, BLACK)
            win.blit(text, (self.x * CELL_DIM + (self.w * CELL_DIM //2  - text.get_width()//2), self.y * CELL_DIM + (self.h * CELL_DIM//2 - text.get_height()//2)))

    def isOver(self, x, y):
        
        x = x // CELL_DIM
        y = y // CELL_DIM
        #print()
        #print(f"{x}, {y}    this object {self.x}, {self.y}")
        #print(f"w {self.w}, h {self.h}")
        if x >= self.x and x < self.x + self.w :
            if y >= self.y and y < self.y + self.h :
                return True

        return False


""" //----------- SLIDER ------------/// """
class Slider:
    
    def __init__(self, x, y, w, h):
         self.circle_x = x 
         self.volume = 0 
         print(x)
         print(y)
         print(w)
         print(h)
         self.sliderRect = pygame.Rect(x - w // 2, y, w, h)

    def draw(self, screen):
        
        pygame.draw.rect(screen, BLACK, self.sliderRect)
        pygame.draw.circle(screen, RED, (self.circle_x, (self.sliderRect.h / 2 + self.sliderRect.y)), self.sliderRect.h * 1.5)

    def get_volume(self):
        return self.volume

    def set_volume(self, num):
        self.volume = num

    def update_volume(self, x):
        if x < self.sliderRect.x:
            self.volume = 0
        elif x > self.sliderRect.x + self.sliderRect.w:
            self.volume = 100
        else:
            self.volume = int((x - self.sliderRect.x) / float(self.sliderRect.w) * 100)

    def on_slider(self, x, y):
        if self.on_slider_hold(x, y) or self.sliderRect.x <= x <= self.sliderRect.x + self.sliderRect.w and self.sliderRect.y <= y <= self.sliderRect.y + self.sliderRect.h:
            return True
        else:
            return False

    def on_slider_hold(self, x, y):
        if ((x - self.circle_x) * (x - self.circle_x) + (y - (self.sliderRect.y + self.sliderRect.h / 2)) * (y - (self.sliderRect.y + self.sliderRect.h / 2)))\
            <= (self.sliderRect.h * 1.5) * (self.sliderRect.h * 1.5):
            return True
        else:
            return False

    def handle_event(self, screen, x):
        if x < self.sliderRect.x:
            self.circle_x = self.sliderRect.x
        elif x > self.sliderRect.x + self.sliderRect.w:
            self.circle_x = self.sliderRect.x + self.sliderRect.w
        else:
            self.circle_x = x
        self.draw(screen)
        self.update_volume(x)
        print(self.volume)



""" //----------- UTILS ------------/// """
class Utils:
    colors = [(255,0,0), (0,187,0), (255,204,102), (255,128,0), (128, 0,128), (0,255,255)]
    
    def makeBoard(self, dim):
        board = []
        for i in range(dim):
            row = []
            for j in range(dim):
                if i == 0 and j == 0:
                    c = Cell(self.colors[randint(0,5)], i, j, True)
                else:
                    c = Cell(self.colors[randint(0,5)], i, j, False)
                row.append(c);
            board.append(row)
        b = Board(board, dim)
        b.floodCells(b.getCell(0,0).color)
        return b
            


        
""" //----------- Cell ------------/// """
class Cell: 

    def __init__(self, color, x, y, flooded):
        self.color = color;
        self.x = x;
        self.y = y;
        self.isFlooded = flooded;
    
    def changeColor(self, color):
        self.color = color
    
    def floodAdjacent(self, color, board):
        x = self.x
        y = self.y

        if self.x <  board.dim - 1:
            c1 = board.getCell(x+1, y)
            if c1.color == color and not c1.isFlooded:
                c1.isFlooded = True
                c1.floodAdjacent(color, board)

        
        if self.y < board.dim - 1:
            c2 = board.getCell(x, y + 1)
            if c2.color == color and not c2.isFlooded:
                c2.isFlooded = True
                c2.floodAdjacent(color, board)
        
       
        if self.x > 0:
            c3 = board.getCell(x - 1, y)
            if c3.color == color and not c3.isFlooded:
                c3.isFlooded = True
                c3.floodAdjacent(color, board)

        
        if self.y > 0:
            c4 = board.getCell(x, y - 1)
            if c4.color == color and not c4.isFlooded:
                c4.isFlooded = True
                c4.floodAdjacent(color, board)
        
            


""" //----------- Board ------------/// """  
class Board:

    def __init__(self, cells, dim):
        self.cells = cells;
        self.dim = dim;
    def drawBoard(self):
        for row in self.cells:
            for cell in row:
                r = pygame.Rect(cell.x * CELL_DIM, cell.y * CELL_DIM, CELL_DIM, CELL_DIM)
                pygame.draw.rect(WINDOW, cell.color, r)
    
    def getCell(self, x, y):
        return self.cells[x][y]

    def floodCells(self, color):
        for row in self.cells:
            for cell in row:
                if cell.isFlooded:
                    # update the color
                    cell.changeColor(color)
                    cell.floodAdjacent(color, self)




# flood it class
class FloodIt:
    u = Utils()
    def __init__(self, board):
        self.board = board;
        self.guesses = board.dim * 2 - board.dim // 4;
        self.guessesLeft = self.guesses;
        self.curColor = self.board.getCell(0,0).color
    
    def __init__(self, dim):
        self.dim = dim;
        self.board = self.u.makeBoard(self.dim)
        self.guesses = 25*((2*dim)*6)//((14+14)*6)
        self.guessesLeft = self.guesses;
        self.curColor = self.board.getCell(0,0).color
        self.rstBtn = Button(0, dim, 4, 2, "RESET", GREY)
        self.slider = Slider(wWIDTH // 2, wHEIGHT - CELL_DIM // 2, CELL_DIM * 5, 5)

    def drawGame(self):
        self.board.drawBoard()
    
    def drawScore(self):
        # if tehre are guesses left
        if self.guessesLeft > 0:
            text  = FONT.render(f"Guesses: {self.guessesLeft} / {self.guesses}", False, (0,0,0))
            WINDOW.blit(text, text.get_rect(center=(wWIDTH // 2,  (wHEIGHT - (wHEIGHT // 10)))))
        else:
            text  = FONT.render(f"You Lose!", False, (0,0,0))
            WINDOW.blit(text, text.get_rect(center=(wWIDTH // 2,  (wHEIGHT - (wHEIGHT // 10))))) 

    
    def onClick(self, x, y):
        #scale down posn
        px = x // CELL_DIM
        py = y // CELL_DIM

        # check if the posn is within board dimensions
        if self.guessesLeft > 0 and px < self.dim and py < self.dim:
            # get the cell color at the position
            cell = self.board.getCell(px, py)
            # determine if a flood is needed
            if self.curColor != cell.color:
                self.floodCells(cell.color)
                self.guessesLeft -= 1
                self.curColor = cell.color
        # if reset button is pressed
        elif self.rstBtn.isOver(x,y):
            # rest the values
            self.board = self.u.makeBoard(self.dim)
            self.guessesLeft = self.guesses;
            self.curColor = self.board.getCell(0,0).color


    def floodCells(self, color):
        self.board.floodCells(color)

    

def draw_window(flood):
    WINDOW.fill(WHITE)
    flood.drawGame()
    flood.drawScore()
    flood.rstBtn.draw(WINDOW, BLACK)
    flood.slider.draw(WINDOW)
    pygame.display.update()


dim = 14
wHEIGHT = 6 * (dim * CELL_DIM) // 5
wWIDTH = dim * CELL_DIM
WINDOW = pygame.display.set_mode((wWIDTH, wHEIGHT))
def main():
    clock = pygame.time.Clock()

    flood = FloodIt(dim)
    
    

    run = True
    while run:
       
        clock.tick(FPS)
        for event in pygame.event.get():
             
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                flood.onClick(mx, my)

                if flood.slider.on_slider(mx,my):
                    flood.slider.handle_event(WINDOW, mx)
                    print(f"Diff {- flood.slider.circle_x // CELL_DIM - flood.slider.sliderRect.x // CELL_DIM } ")

            if flood.rstBtn.isOver(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                flood.rstBtn = Button(0, dim, 4, 2, "RESET", DKGREY)
            else:
                flood.rstBtn = Button(0, dim, 4, 2, "RESET", GREY)
        draw_window(flood)
        #x, y = pygame.display.set_mode((dim * CELL_DIM, dim * CELL_DIM))
        #print(x,y)
    
    pygame.quit()


if __name__ == "__main__":
    main()