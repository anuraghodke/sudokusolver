# STANDARD BACKTRACKING
# expert aprx. 12/13s
import math
import copy

def sudoku(boardFile):
    with open(boardFile) as file:
        lines = file.readlines()
    
    board = []
    for line in lines:
        row = []
        for digit in line:
            if not digit.isspace():
                row.append(int(digit))
        board.append(row)

    printBoard(board)
    soln = sudokuSolver(0, board)
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

def boardIsLegal(pos, digit, board):
    # MAKE DEEPCOPY & INSERT DIGIT AT POS
    boardcp = copy.deepcopy(board)
    row, col = getCD(pos, board)
    boardcp[row][col] = digit

    # rows
    dim = len(boardcp)
    for qrow in range(dim):
        for qcol in range(dim):
            if not boardcp[qrow][qcol] == 0 and boardcp[qrow].count(boardcp[qrow][qcol]) > 1:
                return False

    # cols
    for qcol in range(dim):
        colDigits = []
        for qrow in range(dim):
            colDigits.append(boardcp[qrow][qcol])
        
        for colDigit in colDigits:
            if not colDigit == 0 and colDigits.count(colDigit) > 1:
                return False

    # box
    boxDim = int(math.sqrt(dim))
    coords = []
    for boxRow in range(boxDim):
        for boxCol in range(boxDim):
            coords.append((boxRow * boxDim, boxCol * boxDim))

    for (row, col) in coords:
        boxDigits = []
        for i in range(boxDim):
            for j in range(boxDim):
                boxDigits.append(boardcp[row + i][col + j])

        for boxDigit in boxDigits:
            if not boxDigit == 0 and boxDigits.count(boxDigit) > 1:
                return False
    return True

def sudokuSolver(pos, board):
    dim = len(board)
    if (pos == dim * dim):
        return board
    else:
        row, col = getCD(pos, board)
        if board[row][col] == 0:
            for digit in range(1, 10):
                if boardIsLegal(pos, digit, board):
                    board[row][col] = digit
                    solution = sudokuSolver(pos + 1, board)
                    if (solution != None):
                        return solution
                    board[row][col] = 0
            return None
        else:
            return sudokuSolver(pos + 1, board)

if __name__ == "__main__":
    filename = input("Enter board file name: ")
    sudoku(filename)