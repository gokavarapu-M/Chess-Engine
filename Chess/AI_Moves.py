import random

'''
Zero-Sum Game White as muchas positive, Black as much as negative
'''
pieceScore = {"K":0,"Q":10,"R":5,"B":3,"N":3,"p":1}
CHECKMATE = 1000
STALEMATE = 0

'''
Random Mover
Generates a random move from the list of valid moves
'''

def findRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]

'''
Find the best move based on material alone
'''

def findBestMove(gs,validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves) #randomise the moves to avoid the same moves being played
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentMoves = gs.getValidMoves()
        opponentMaxScore = -CHECKMATE
        if gs.checkmate:
            opponentMaxScore = -CHECKMATE
        elif gs.stalemate:
            opponentMaxScore = STALEMATE
        else:
            for opponentMove in opponentMoves: #we are calculating the score of the opponent
                gs.makeMove(opponentMove)
                gs.getValidMoves()
                if gs.checkmate:
                    score = CHECKMATE
                elif gs.stalemate:
                    score = STALEMATE
                else: 
                    score = -turnMultiplier*scoreMaterial(gs.board)# negative when black turn and positive when white turn
                if score > opponentMaxScore:
                    opponentMaxScore = score
                gs.undoMove()
            #minimisation
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    
    return bestPlayerMove

'''
Score the board based on material
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]

    return score