import random

'''
Zero-Sum Game White as muchas positive, Black as much as negative
'''
pieceScore = {"K":0,"Q":10,"R":5,"B":3,"N":3,"p":1}

knightScores = [[1,1,1,1,1,1,1,1],
                [1,2,2,2,2,2,2,1],
                [1,2,3,3,3,3,2,1],
                [1,2,3,4,4,3,2,1],
                [1,2,3,4,4,3,2,1],
                [1,2,3,3,3,3,2,1],
                [1,2,2,2,2,2,2,1],
                [1,1,1,1,1,1,1,1]]
bishopScores = [[4,3,2,1,1,2,3,4],
                [3,4,3,2,2,3,4,3],
                [2,3,4,3,3,4,3,2],
                [1,2,3,4,4,3,2,1],
                [1,2,3,4,4,3,2,1],
                [2,3,4,3,3,4,3,2],
                [3,4,3,2,2,3,4,3],
                [4,3,2,1,1,2,3,4]]
queenScores = [[1,1,1,3,1,1,1,1],
                [1,2,3,3,3,3,2,1],
                [1,3,3,4,4,3,3,1],
                [3,3,4,4,4,4,3,3],
                [1,3,4,4,4,4,3,1],
                [1,3,3,4,4,3,3,1],
                [1,2,3,3,3,3,2,1],
                [1,1,1,3,1,1,1,1]]
rookScores = [[4,3,4,4,4,4,3,4],
                [4,4,4,4,4,4,4,4],
                [1,1,2,3,3,2,1,1],
                [1,2,3,4,4,3,2,1],
                [1,2,3,4,4,3,2,1],
                [1,1,2,3,3,2,1,1],
                [4,4,4,4,4,4,4,4],
                [4,3,4,4,4,4,3,4]]
whitePawnScores = [[8,8,8,8,8,8,8,8],
                   [8,8,8,8,8,8,8,8],
                   [5,6,6,7,7,6,6,5],
                   [2,3,3,5,5,3,3,2],
                   [1,2,3,4,4,3,2,1],
                   [1,2,3,3,3,3,2,1],
                   [1,1,1,0,0,1,1,1],
                   [0,0,0,0,0,0,0,0]]
blackPawnScores = [[0,0,0,0,0,0,0,0],
                    [1,1,1,0,0,1,1,1],
                    [1,2,3,3,3,3,2,1],
                    [1,2,3,4,4,3,2,1],
                    [2,3,3,5,5,3,3,2],
                    [5,6,6,7,7,6,6,5],
                    [8,8,8,8,8,8,8,8],
                    [8,8,8,8,8,8,8,8]]
piecePositionScores = {"N":knightScores,"B":bishopScores,"Q":queenScores,"R":rookScores,"wp":whitePawnScores,"bp":blackPawnScores}



CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2
'''
Random Mover
Generates a random move from the list of valid moves
'''

def findRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]

'''
Find the best move based on material alone
MinMax without recursion
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
Helper method to make the first recursive call
'''

def findBestMoveMinMax(gs,validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    # findMoveMinMax(gs,validMoves, DEPTH, gs.whiteToMove)
    findMoveNegaMaxAlphaBeta(gs,validMoves, DEPTH,-CHECKMATE,CHECKMATE, 1 if gs.whiteToMove else -1)
    return nextMove


def findMoveMinMax(gs,validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    random.shuffle(validMoves)
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs,nextMoves,depth-1,False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs,nextMoves,depth-1,True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore
    

''''
Same as MinMax algorithm but this uses variable turnMultiplier to determine the minscore and maxscore in one function
'''
def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier*scoreBoard(gs)
    random.shuffle(validMoves)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs,nextMoves,depth-1,-turnMultiplier) #negative because we are looking at the opponent's score
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore

''''
Alpha Beta Pruning
if we already have a better move, we can stop there because we already got a better move of opponent and this will reduce nodes in the tree
'''


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth,alpha,beta,turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier*scoreBoard(gs)
    # move ordering - implement later
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs,nextMoves,depth-1,-beta,-alpha,-turnMultiplier) #negative because we are looking at the opponent's score
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha: #pruning happens here
            alpha = maxScore
        
        if alpha >= beta:
            break
    return maxScore


'''
Positive score is good for white, negative score is good for black
'''
    

def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE #black wins
        else:
            return CHECKMATE #white wins
    elif gs.stalemate:
        return STALEMATE
    
    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                piecePositionScore = 0
                if square[1]!="K":
                    if square[1]=="p":
                        piecePositionScore = piecePositionScores[square][row][col]
                    else:
                        piecePositionScore = piecePositionScores[square[1]][row][col]
            if square[0] == 'w':
                score += pieceScore[square[1]] + piecePositionScore* .1
            elif square[0] == 'b':
                score -= pieceScore[square[1]] + piecePositionScore* .1
    return score
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