'''
Main driver file. Responsible fro handling user input and displaying the current GameState
'''

import pygame as p
import ChessEngine


WIDTH = HEIGHT = 512 # height and width of the window
DIMENSION = 8 #dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #speed of animation on screen
IMAGES = {} 
'''
Intialize a global dictionary of images. THis will be called exactly once in main
Need not call images every time which makes game fast
'''

def loadImages():
    pieces = ['wR','wp','wN','wB','wK','wQ','bp','bR','bN','bB','bK','bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"),(SQ_SIZE,SQ_SIZE))
        #transform image into size of square
        
    #stored images in variables now images can be accessed with "IMAGES[piece]"

'''
The main driver for our code. This will handle user input and updating the graphics according to moves
'''

def main():
    p.init() #intializes all necessary modules in pygame
    screen = p.display.set_mode((WIDTH, HEIGHT)) #create a screen
    clock = p.time.Clock() #create a clock, used to measure time taken by each player
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made, this helps to create new valid moves

    # print(gs.board)
    loadImages() #only do this once, before the while loop
    running = True
    sqSELECTED = () #no square is selected initially, keep track of last click of user (tuple: (row,col))
    playerClicks = [] #keep track of player clicks (tuple of two positions)
    
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN: #mouse is clicked
                location = p.mouse.get_pos() #(x,y) location of mouse
                col = location[0]//SQ_SIZE   #get column
                row = location[1]//SQ_SIZE   #get row
                if sqSELECTED == (row,col): #undo when clicked on same square twice
                    sqSELECTED = () #deselect
                    playerClicks = [] #clear player clicks
                else:
                    sqSELECTED = (row,col)
                    playerClicks.append(sqSELECTED) #append for both 1st and 2nd clicks
                if len(playerClicks) == 2: #after 2nd click
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSELECTED = () #reset user clicks
                        playerClicks = []
                    else:
                        playerClicks = [sqSELECTED]

            #key handler
            elif e.type == p.KEYDOWN:   #undo when 'z' is pressed
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade: 
            validMoves = gs.getValidMoves()
            moveMade = False
        
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

## Graphics on Board
def drawGameState(screen, gs):
    drawBoard(screen) #draw squares on board
    # add piece highligthing later
    drawPieces(screen,gs.board)

def drawBoard(screen):
    ##draw squares
    colors = [p.Color("white"),p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE)) 

def drawPieces(screen, board):
    ##draw pieces
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))


if __name__ == "__main__":
    main()
