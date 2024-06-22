'''
storing info about the current state of game
Responsible for determining valid moves, also keep a move log
'''
class GameState():
    def __init__(self):
        # board is 8X8 2D list, each element has 2 characters
        # first character is color and second character is the type of piece
        # "--" empty space with no piece
        '''
        R --> Rook
        N --> Knight
        B --> Bishop
        Q --> Queen
        K --> King
        p --> Pawn
        '''
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ] #8X8 board

        self.moveFunctions = {'p':self.getPawnMoves,'R':self.getRookMoves, 'N':self.getKnightMoves,
                              'B':self.getBishopMoves, 'Q':self.getQueenMoves,'K':self.getKingMoves}
         #dictionary to call functions based on piece type
        self.whiteToMove = True #keep track of which player has to move
        self.movelog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkMate = False
        self.staleMate = False


    # takes a move as a parameter and executes it (this will not work for castling, pawn promotion and en-passant)
    def makeMove(self,move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move) #log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove #swap players
        #update the king's location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow,move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow,move.endCol)

    # undo the last move made
    def undoMove(self):
        if len(self.movelog) != 0: #make sure that there is a move to undo
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #give turn back to the original player
            #update the king's location is changed after undo
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow,move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow,move.startCol)
    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        '''
        "Need to be updated" (inefficient way to get valid moves)
        1. Get all possible moves
        '''
        moves = self.getAllPossibleMoves()
        '''
        2. For each move, make the move
        '''
        for i in range(len(moves)-1,-1,-1): #when removing from a list, go backwards
            self.makeMove(moves[i])
            '''
        3. Generate all the opponent's moves
        4. For each of your opponent's moves, see if any of them attack your king
            '''
            self.whiteToMove = not self.whiteToMove #this is because makeMove changes the player
            if self.inCheck():
                moves.remove(moves[i]) #if in check, remove the move
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        return moves

    #checks if the current player is in check
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])

    
    #checks if enemy can attack the square r,c
    def squareUnderAttack(self,r,c):
        self.whiteToMove = not self.whiteToMove #switch to opponent's turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False
    
    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0] #w or b (first character of the string)
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1] #type of piece
                    self.moveFunctions[piece](r,c,moves) #call appropriate move function based on piece type
        return moves

    #pawn moves
    #pawn promotions not added
    def getPawnMoves(self,r,c,moves):
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == "--": #1 square pawn advance
                moves.append(Move((r,c),(r-1,c),self.board))
                if r == 6 and self.board[r-2][c] == "--": #2 square pawn advance
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1 >= 0: #captures to the left
                if self.board[r-1][c-1][0] == 'b': #enemy piece to capture
                    moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1 <= 7: #captures to the right
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c),(r-1,c+1),self.board))
        else: #black pawn moves
            if self.board[r+1][c] == "--": #1 square pawn advance
                moves.append(Move((r,c),(r+1,c),self.board))
                if r == 1 and self.board[r+2][c] == "--": #2 square pawn advance
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1 >= 0: #captures to the right
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1 <= 7: #captures to the left
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c+1),self.board))
    #rook moves
    def getRookMoves(self,r,c,moves):
        directions = ((-1,0),(0,-1),(1,0),(0,1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty space
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0] == enemyColor: #enemy piece
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else: #same color
                        break
                else: #off board
                    break
                
    #knight moves
    def getKnightMoves(self,r,c,moves):
        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #not same color piece 
                    moves.append(Move((r,c),(endRow,endCol),self.board))
                
    #bishop moves
    def getBishopMoves(self,r,c,moves):
        directions = ((-1,-1),(-1,1),(1,-1),(1,1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty space
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0] == enemyColor: #enemy piece
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else: #same color
                        break
                else: #off board
                    break

    #queen moves
    def getQueenMoves(self,r,c,moves):
        # queen can move like a rook and a bishop
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)
    #king moves
    def getKingMoves(self,r,c,moves):
        kingMoves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in kingMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #not same color piece 
                    moves.append(Move((r,c),(endRow,endCol),self.board))



class Move():
    # maps keys to values
    # key : value
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0} #reverse order because white is at the bottom
    rowsToRanks = {v:k for k,v in ranksToRows.items()}
    filesToCols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFiles = {v:k for k,v in filesToCols.items()}


    def __init__ (self,startSq,endSq,board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveId = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
        # print(self.moveId)

    '''
    Overriding the equals method
    '''
    def __eq__(self,other): #equality checker for checking in valid moves
        if isinstance(other,Move):
            return self.moveId == other.moveId
        return False
    
    def getChessNotation(self):
        # you can add to make this real chess notation
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)
    
    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    