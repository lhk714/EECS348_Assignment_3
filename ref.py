# Ang Shen      asi031
# Jaxiao Ma     jmq856
# Huaipei Lu    hlv624


#!/usr/bin/env python
import struct, string, math
from copy import*

class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""

    def __init__(self, size, board):
      """the constructor for the SudokuBoard"""
      self.BoardSize = size #the size of the board
      self.CurrentGameBoard= board #the current state of the game board

    def set_value(self, row, col, value):
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""

        #add the value to the appropriate position on the board
        self.CurrentGameBoard[row][col]=value
        #return a new board of the same size with the value added
        return SudokuBoard(self.BoardSize, self.CurrentGameBoard)


    def print_board(self):
        """Prints the current game board. Leaves unassigned spots blank."""
        div = int(math.sqrt(self.BoardSize))
        dash = ""
        space = ""
        line = "+"
        sep = "|"
        for i in range(div):
            dash += "----"
            space += "    "
        for i in range(div):
            line += dash + "+"
            sep += space + "|"
        for i in range(-1, self.BoardSize):
            if i != -1:
                print "|",
                for j in range(self.BoardSize):
                    if self.CurrentGameBoard[i][j] > 9:
                        print self.CurrentGameBoard[i][j],
                    elif self.CurrentGameBoard[i][j] > 0:
                        print "", self.CurrentGameBoard[i][j],
                    else:
                        print "  ",
                    if (j+1 != self.BoardSize):
                        if ((j+1)//div != j/div):
                            print "|",
                        else:
                            print "",
                    else:
                        print "|"
            if ((i+1)//div != i/div):
                print line
            else:
                print sep

def parse_file(filename):
    """Parses a sudoku text file into a BoardSize, and a 2d array which holds
    the value of each cell. Array elements holding a 0 are considered to be
    empty."""

    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val

    return board

def is_complete(sudoku_board):
    """Takes in a sudoku board and tests to see if it has been filled in
    correctly."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    #check each cell on the board for a 0, or if the value of the cell
    #is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col]==0:
                return False
            for i in range(size):
                if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                    return False
                if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                    return False
            #determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == BoardArray[row][col])
                        and (SquareRow*subsquare + i != row)
                        and (SquareCol*subsquare + j != col)):
                        return False
    return True

def init_board(file_name):
    """Creates a SudokuBoard object initialized with values from a text file"""
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)

def backTracking(sudoku_board):
    """Implements backtracking algorithm"""
    if is_complete(sudoku_board):
        return sudoku_board
    else:
        row, col = unassignedVar(sudoku_board)
        D = [i+1 for i in range(sudoku_board.BoardSize)]
        for val in D:
            #count += 1
            if isconsistent(sudoku_board, row, col, val):
                sudoku_board.set_value(row, col, val)
                result = backTracking(sudoku_board)
                if result != False:
                    return result
                else:
                    sudoku_board.set_value(row, col, 0)
        return False

def unassignedVar(sudoku_board):
    """Returns row and col of a empty node, otherwise returns False"""
    size = sudoku_board.BoardSize
    BoardArray = sudoku_board.CurrentGameBoard
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col] == 0:
                return row,col
    return False

def isconsistent(sudoku_board, row, col, val):
    """Checks whether a node is consistent, return T or F"""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    startRow = row-row%subsquare
    startCol = col-col%subsquare
    # check a row
    for i in range(size):
        if BoardArray[row][i] == val:
            return False
    # check a column
    for j in range(size):
        if BoardArray[j][col] == val:
            return False
    # check a subsquare
    for subrow in range(subsquare):
        for subcol in range(subsquare):
            if BoardArray[subrow+startRow][subcol+startCol] == val:
                return False
    return True

def forwardConsistentCheck(sudoku_board, checkingTable, row, col, val):
    """Validate a move by finding checking table before the move is actually made, return T or F"""
    size = sudoku_board.BoardSize
    Board = deepcopy(sudoku_board)
    board = Board.CurrentGameBoard
    table = deepcopy(checkingTable)
    board[row][col] = val
    # updates checking table
    table = updateTable(Board, table, row, col, val, size)
    # check checking taboe
    valid = validateCheckingTable(Board, table)
    return valid

def forwardCheckingInit(sudoku_board):
    """Initializes a checking table containing valid values of each node"""
    size = sudoku_board.BoardSize
    BoardArray = sudoku_board.CurrentGameBoard
    checkingTable = ([[[i+1 for i in range(size)] for j in range(size)] for k in range(size)])
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col] != 0:
                val = BoardArray[row][col]
                checkingTable = updateTable(sudoku_board, checkingTable, row, col, val, size)
    return checkingTable

def updateTable(sudoku_board, table, row, col, val, size):
    """Updates checking table, assign a value to a node, eliminate the value from its neighbours"""
    size = sudoku_board.BoardSize
    BoardArray = sudoku_board.CurrentGameBoard
    table[row][col] = [val]
    for i in range(size):
        for j in range(size):
            if i!=row or j!=col:
                if BoardArray[i][j] == 0:
                    if consistencyCheck(i, j, row, col, size):
                        if val in table[i][j]:
                            table[i][j].remove(val)
    return table

def validateCheckingTable(sudoku_board, checkingTable):
    """Validate checking table by finding any value with emtpy value options"""
    size = sudoku_board.BoardSize
    BoardArray = sudoku_board.CurrentGameBoard
    for i in range(size):
        for j in range(size):
            if BoardArray[i][j] == 0:
                if checkingTable[i][j] == []:
                    return False
    return True

def consistencyCheck(i, j, row, col, size):
    """Checks if two nodes are consistent with each other"""
    subsquare = int(math.sqrt(size))
    startRow = row-row%subsquare
    startCol = col-col%subsquare
    if (i == row) or (j == col) or ((i-startRow>=0) and (i-startRow<subsquare) and (j-startCol>=0) and (j-startCol<subsquare)):
        return True
    return False

def forwardChecking(sudoku_board, MRV_h, MCV_h, LCV_h):
    """Top-level forward checking function"""
    #count = 0
    initTable = forwardCheckingInit(sudoku_board)
    result = forwardChecking_rec(sudoku_board, initTable, MRV_h, MCV_h, LCV_h)
    return result

def forwardChecking_rec(sudoku_board, checkingTable, MRV_h, MCV_h, LCV_h):
    """Forwarding checking recursion function"""
    # return if board is completed
    if is_complete(sudoku_board):
        return sudoku_board
    # return if checking table is not valid
    if (not validateCheckingTable(sudoku_board, checkingTable)):
        return False

    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    # find an emtpy node from board
    if MRV_h == True:
        row, col = MRV_func(sudoku_board, checkingTable)
    elif MCV_h == True:
        row, col = MCV_func(sudoku_board)
    else:
        row, col = unassignedVar(sudoku_board)

    # Creats a list of legal values of given node
    if LCV_h == True:
        D = LCV_func(sudoku_board, row, col, checkingTable)
    else:
        D = [i for i in checkingTable[row][col]]

    for val in D:
        #count += 1
        if forwardConsistentCheck(sudoku_board, checkingTable, row, col, val):
            if isconsistent(sudoku_board, row, col, val):
                sudoku_board.set_value(row, col, val)
                checkingTable = updateTable(sudoku_board, checkingTable, row, col, val, size)
                result = forwardChecking_rec(sudoku_board, checkingTable, MRV_h, MCV_h, LCV_h)
                if result != False:
                    return result
                else:
                    sudoku_board.set_value(row, col, 0)
                    checkingTable = forwardCheckingInit(sudoku_board)
    return False

def MRV_func(sudoku_board, checkingTable):
    """Finds an empty node that has the fewest legal moves"""
    size = sudoku_board.BoardSize
    BoardArray = sudoku_board.CurrentGameBoard
    min_val = 1000
    for i in range(size):
        for j in range(size):
            if BoardArray[i][j] == 0:
                tmp = len(checkingTable[i][j])
                if  tmp < min_val:
                    min_val = tmp
                    row = i
                    col = j
    print row, col, min_val
    x = raw_input("=======")
    return row, col

def MCV_func(sudoku_board):
    """Finds an emtpy node that has the imposes the most constraints on other nodes """
    size = sudoku_board.BoardSize
    BoardArray = sudoku_board.CurrentGameBoard
    max_val = -1000
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col] == 0:
                count = countConsistnecy(sudoku_board, row, col)
                if count > max_val:
                    max_val = count
                    ii = row
                    jj = col
    return ii, jj

def countConsistnecy(sudoku_board, row, col):
    """Count the number of neighbours of a given node"""
    size = sudoku_board.BoardSize
    BoardArray = sudoku_board.CurrentGameBoard
    count = 0
    for i in range(size):
        for j in range(size):
            if not(i == row and j == col):
                if BoardArray[i][j] == 0:
                    if consistencyCheck(i,j,row,col,size):
                        count += 1
    return count

def LCV_func(sudoku_board, row, col, checkingTable):
    """Choose the value that filters out fewest values in neighbours"""
    size = sudoku_board.BoardSize
    BoardArray = sudoku_board.CurrentGameBoard
    curValLst = checkingTable[row][col]
    vals = []
    diffs = []
    for val in curValLst:
        nt = deepcopy(checkingTable)
        total_prev = calcTotal(BoardArray, nt, row, col, size)
        nt = updateTable(sudoku_board, nt, row, col, val, size)
        total_next = calcTotal(BoardArray, nt, row, col, size)
        diff = total_prev-total_next
        vals.append(val)
        diffs.append(diff)

    D = [x for (y,x) in sorted(zip(diffs,vals))]
    return D

def calcTotal(BoardArray, checkingTable, row, col, size):
    """Calculates the total number of value options of all the neighbours of a given node"""
    total = 0
    for i in range(size):
        for j in range(size):
            if (BoardArray[i][j]==0) and (i!=row | j!= col):
                tmp = len(checkingTable[i][j])
                total += tmp
    return total


def solve(initial_board, forward_checking = False, MRV = False, MCV = False,
    LCV = False):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
    myBoard = deepcopy(initial_board)
    if forward_checking == True:
        myBoard = forwardChecking(myBoard, MRV, MCV, LCV)
    else:
        myBoard = backTracking(myBoard)
    return myBoard
