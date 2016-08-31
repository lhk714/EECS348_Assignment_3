#!/usr/bin/env python
import struct, string, math
from copy import deepcopy

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

def solve(initial_board, forward_checking = False, MRV = False, Degree = False, LCV = False):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """

    # print "Your code will solve the initial_board here!"
    # print "Remember to return the final board (the SudokuBoard object)."
    # print "I'm simply returning initial_board for demonstration purposes."
    # return initial_board
    sudoku_board = deepcopy(initial_board) # create a new board
    global numOfConsistencyCheck  # global variable to store the number of consistency check
    numOfConsistencyCheck = 0  # initiate the global variable
    if forward_checking == True:
        print "======forward_checking( MRV =",MRV,", Degree =",Degree, ", LCV =", LCV,")======"
        sudoku_board = forwardChecking(sudoku_board, MRV, Degree, LCV)  # forward checking with different heuristics
    else:
        print "======back_tracking======"
        sudoku_board = backTracking(sudoku_board)  # back tracking only = depth-first-search

    print "Number of consistency checks =", numOfConsistencyCheck
    return sudoku_board  # return the solved sudoku board


def backTracking (sudoku_board):
    """Implement of backtracking"""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)  # get the size of the board
    if is_complete(sudoku_board) == True:
        return sudoku_board
    else:
        row, col = findEmptyPosition(sudoku_board)  # find an empty spot on the board
        for i in range(size):
            global numOfConsistencyCheck
            numOfConsistencyCheck += 1  # update the global variable
            value = i +1  # set the value of the spot
            if checkBackTrackingConsistency(sudoku_board, row, col, value):  # consistency checking
                sudoku_board.set_value(row, col, value)  # update the sudoku board
                result = backTracking(sudoku_board)  # recursive calling
                if result != None:
                    return result
                else:
                    sudoku_board.set_value(row, col, 0)  # found inconsistency, reset the value of that spot
        return None  # back tracking return


def findEmptyPosition(sudoku_board):
    """return row and col of an empty spot"""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col] == 0:  # where 0 indicates there is a empty spot
                return row, col
    return None, None  # no empty spot found

def checkBackTrackingConsistency(sudoku_board, row, col, value):
    """check the consistency of spot [row,col]= value"""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subSize = int(math.sqrt(size))  # size of the sub_board
    subRow = row - row%subSize  # start row num of the sub_board
    subCol = col - col%subSize  # start col num of the sub_board

    # check row consistency in the whole board
    for i in range(size):
        if BoardArray[i][col] == value: # check row consistency in the whole board
            return False
        elif BoardArray[row][i] == value: # check column consistency in the whole board
            return False

     # check consistency in the sub board
    for i in range(subSize):
        for j in range(subSize):
            if BoardArray[i + subRow][j + subCol] == value:
                return False
    return True  # the board is consistent


def forwardChecking(sudoku_board, MRV, Degree, LCV):
    """Implement of forwardchecking"""
    table = forwardCheckingTable(sudoku_board)  # construct a table contains the values of spots which are forward consistent
    board = forwardCheckingHelper(sudoku_board,table, MRV, Degree, LCV)  # forward checking with different heuristic algorithm, return a complete sudoku board
    return board

def forwardCheckingTable(sudoku_board):
    """build a table containing valid values of each spot"""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    """
     initiate a data structure (table) to store all the possible values for the spots on the sudoku board
     eg. for 4*4 board, the data structure is a 4*4 table with  each row and column corresponding
     to the configuration of the sudoku board, and each tuple stores 4 values: 1,2,3 and 4
     Later on, the heuristic algorithm will delete those inconsistent values of the data structure
     The final remaining result is the solution of the sudoku board
    """
    table = [[[k+1 for k in range(size)] for i in range(size)] for k in range(size)]
    for row in range(size):
        for col in range(size):
            value = BoardArray[row][col]
            if value !=0:
                table = updateTable(sudoku_board, table, row, col, value)  # forward checking to remove inconsistent values in the table
    return table  # return the forward-checking consistent table

def updateTable(sudoku_board, table, row, col, value):
    """update the table: assign value to a spot based on the current configuration of the sudoku board and remove inconsistency"""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    table[row][col] = [value]  # set the value to the table (remove other values)
    for i in range(size):
        for j in range(size):
            if i != row or j != col:
                if BoardArray[i][j] == 0:  # unassigned spot
                    if checkSpotConsistency(row, col, i, j, size): # check whether the spot(row, col) effects spot(i,j)
                        if value in table[i][j]:  # the spot contains the same value
                            table[i][j].remove(value)  # remove the value from that spot
    return table

def checkSpotConsistency(row, col, i, j, size):
    """Checks if two spot are related with each other"""
    subSize = int(math.sqrt(size))
    subRow = row - row % subSize
    subCol = col - col % subSize
    # check if 2 spots are in the same row or the same column or the same sub-board
    if (i == row) or (j == col) or ((i - subRow >= 0) and (i - subRow < subSize) and (j - subCol >= 0) and (j - subCol < subSize)):
        return True
    else:
        return False

def forwardCheckingHelper(sudoku_board, table, MRV, Degree, LCV):
    """recursive forwarding checking and back tracking"""
    if is_complete(sudoku_board):
        return sudoku_board
    if not validateTable(sudoku_board, table):  # no solution to the current board configuration
        return False

    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)

    if MRV == True: # MRV (minimum remaining values) Heuristic - choose the variable with the fewest values left
        row, col = MRVHelper(sudoku_board, table)
    elif Degree == True:  # Degree Heuristic - choose the variable that is involved in the largest number of constraints on unassigned variables
        row, col = DegreeHelper(sudoku_board)
    else:  # forward checking without heuristic
        row, col = findEmptyPosition(sudoku_board)  # find an empty spot. the same as used in back tracking

    if LCV == True: # LCV (least constraining value) Heuristic - choose the value that rules out the fewest choices for other unassigned variables
        list = LCVHelper(sudoku_board, row, col, table)
    else: # test all the possible values
        list = [i for i in table[row][col]]

    for value in list:
        global numOfConsistencyCheck
        numOfConsistencyCheck += 1  # update the global variable
        if checkForwardCheckingConsistency(sudoku_board, table, row, col, value):  # check a move in forward-checking
            if checkBackTrackingConsistency(sudoku_board, row, col, value):  # check back-tracking consistency
                sudoku_board.set_value(row, col, value)  # set spot(row, col) = value, which is consistent in both forward-checking and back-tracking
                table = updateTable(sudoku_board, table, row, col, value)  # update the data structure
                result = forwardCheckingHelper(sudoku_board, table,MRV,Degree,LCV)  # recursively move to the next move
                if result != False:
                    return result  #  the solution is found
                else:
                    sudoku_board.set_value(row, col, 0)  # reset the board
                    table = forwardCheckingTable(sudoku_board)  # reset the table
    return False

def validateTable(sudoku_board, table):
    """Validate table: if finding spot with no value options, current moves lead failure"""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col] == 0:
                if table[row][col] ==[]:  # the spot contains no available values
                    return False
    return True

def MRVHelper(sudoku_board, table):
    """ MRV (minimum remaining values) Heuristic - choose the variable with the fewest values left"""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    minValue = 1.0e400  # minValue stores the number of available values
    for i in range(size):
        for j in range(size):
            if BoardArray[i][j] == 0:
                tmp = len(table[i][j])
                if tmp < minValue:
                    minValue = tmp
                    row = i
                    col = j
    return row, col  # found the spot(row, col) with minimal remaining values


def DegreeHelper(sudoku_board):
    """Degree Heuristic - choose the variable that is involved in the largest number of constraints on unassigned variables"""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    maxValue = -1.0e400  # maxValue stores the number of unassigned neighbor spot of current spot
    for i in range(size):
        for j in range(size):
            if BoardArray[i][j] == 0:
                count = countUnassignedNeighbors(sudoku_board, i, j)  # count the number of unassigned neighbor spots
                if count > maxValue:
                    maxValue = count
                    row = i
                    col = j
    return row, col  # found the spot(row, col) with maximal unassigned neighbor spots

def countUnassignedNeighbors(sudoku_board, row, col):
    """Count the number of unassigned neighbours of a given spot"""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    count = 0
    for i in range(size):
        for j in range(size):
            if not (i == row and j == col):
                if BoardArray[i][j] == 0:
                    if checkSpotConsistency(row, col, i, j, size): # Checks if spot(row, col) is related to spot(i,j)
                        count += 1
    return count

def LCVHelper(sudoku_board, row, col, table):
    """LCV (least constraining value) Heuristic - choose the value that rules out the fewest choices for other unassigned variables"""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    values = table[row][col]
    valueList = []  # a list contains values of a spot which rules out the fewest choices for other unassigned spots to the most
    diffenceList = []  # a list contains difference of choices for other unassigned spots before value assignment and after value assignment
    for val in values:
        tb = deepcopy(table)  # make a new table
        countBefore = countValues(BoardArray, tb, row, col, size)  # count the total number of values of all the neighbours of a spot
        tb = updateTable(sudoku_board, tb, row, col, val)  # assignment a value = updade the table
        countAfter = countValues(BoardArray, tb, row, col, size)  # count the total number of values of all the neighbours of a spot
        difference = countBefore - countAfter  # calculate the difference
        valueList.append(val)
        diffenceList.append(difference)

    list = [x for (y,x) in sorted(zip(diffenceList, valueList))]  # construct (diff, val) pair, sort descently based on diff, and return a list of corrsponding values
    return list

def countValues(BoardArray, table, row, col, size):
    """Calculates the total number of values of all the neighbours of a spot"""
    count = 0
    for i in range(size):
        for j in range(size):
            if BoardArray[i][j] == 0 and (i != row or j != col):  # find a neighbor spot
                tmp = len(table[i][j])  # get the number of available values
                count += tmp
    return count


def checkForwardCheckingConsistency(sudoku_board, table, row, col, value):
    """check a move in forward checking"""
    board = deepcopy(sudoku_board) # make a new board
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    tb = deepcopy(table) # make a new table
    BoardArray[row][col] = value  # set spot(row, col) = value
    tb = updateTable(board, tb, row, col, value)  # update table
    isValid = validateTable(board, tb)  # validating the table, return True or False
    return isValid






