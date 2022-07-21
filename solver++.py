# STANDARD BACKTRACTING W CSP w/o constraint
# expert aprx. 3/4s
import math
import copy

def sudoku(boardFile):
    with open(boardFile) as file:
        lines = file.readlines()
    
    #initialize board
    board = []
    for line in lines:
        row = []
        for digit in line:
            if not digit.isspace():
                row.append(int(digit))
        board.append(row)

    #initialize guesses w/ unary constraints
    guesses =  []
    for pos in range(0, 81):
        row, col = getCD(pos, board)
        if board[row][col] == 0:
            rowDigits = getRow(row, board)
            colDigits = getCol(col, board)
            boxDigits = getBox(row, col, board)

            posGuesses = []
            for digit in range(0, 10):
                if not digit in rowDigits and not digit in colDigits and not digit in boxDigits:
                    posGuesses.append(digit)
            guesses.append(posGuesses)
        else:
            guesses.append([])

    printBoard(board)
    soln = sudokuSolver(0, board, guesses)
    print("SOLN:")
    printBoard(soln)

def getPos(row, col, board):
    dim = len(board)
    return row * dim + col

def getCD(pos, board):
    dim = len(board)
    row = pos // dim
    col = pos % dim
    return (row, col)

def printBoard(board):
    if board:
        for row in board:
            print(row)
    else:
        print("NONE")

def getCol(col, board):
    colDigits = []
    dim = len(board)
    for qrow in range(dim):
        colDigits.append(board[qrow][col])
    return colDigits

def getRow(row, board):
    return board[row]

def getBox(row, col, board):
    dim = len(board)
    boxDim = int(math.sqrt(dim))

    row = (row // boxDim) * boxDim
    col = (col // boxDim) * boxDim
    boxDigits = []
    for i in range(boxDim):
        for j in range(boxDim):
            boxDigits.append(board[row + i][col + j])
    return boxDigits

def boardIsLegal(pos, digit, board):
    # MAKE DEEPCOPY & INSERT DIGIT AT POS
    boardcp = copy.deepcopy(board)
    row, col = getCD(pos, board)
    boardcp[row][col] = digit

    dim = len(boardcp)
    boxDim = int(math.sqrt(dim))

    # rows
    for qrow in range(dim):
        rowDigits = getRow(qrow, boardcp)
        for rowDigit in rowDigits:
            if not rowDigit == 0 and rowDigits.count(rowDigit) > 1:
                return False

    # cols
    for qcol in range(dim):
        colDigits = getCol(qcol, boardcp)
        for colDigit in colDigits:
            if not colDigit == 0 and colDigits.count(colDigit) > 1:
                return False

    # box
    coords = []
    for boxRow in range(boxDim):
        for boxCol in range(boxDim):
            coords.append((boxRow * boxDim, boxCol * boxDim))

    for (row, col) in coords:
        boxDigits = getBox(row, col, boardcp)
        for boxDigit in boxDigits:
            if not boxDigit == 0 and boxDigits.count(boxDigit) > 1:
                return False

    return True

def sudokuSolver(pos, board, guesses):
    dim = len(board)
    if (pos == dim * dim):
        return board
    else:
        row, col = getCD(pos, board)
        if board[row][col] == 0:
            for digit in guesses[pos]:
                if boardIsLegal(pos, digit, board):
                    # remove other guesses
                    newGuesses = copy.deepcopy(guesses)
                    for posi in range(0, 81):
                        rowi, coli = getCD(posi, board)
                        dim = len(board)
                        boxDim = int(math.sqrt(dim))
                        boxrow = (row // boxDim) * boxDim
                        boxcol = (col // boxDim) * boxDim
                        boxrowi = (rowi // boxDim) * boxDim
                        boxcoli = (coli // boxDim) * boxDim
                        if (newGuesses[posi].count(digit) > 0) and (row == rowi 
                            or col == coli 
                            or (boxrow == boxrowi and boxcol == boxcoli)):
                                newGuesses[posi].remove(digit)

                    board[row][col] = digit
                    solution = sudokuSolver(pos + 1, board, newGuesses)
                    if (solution != None):
                        return solution
                    board[row][col] = 0
            return None
        else:
            return sudokuSolver(pos + 1, board, guesses)

if __name__ == "__main__":
    filename = input("Enter board file name: ")
    sudoku(filename)