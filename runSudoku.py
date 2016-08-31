import SudokuStarter
execfile("SudokuStarter.py")
sb = SudokuStarter.init_board("input_puzzles/easy/16_16.sudoku")
fb = SudokuStarter.solve(sb, 1, 0, 1, 0)
fb.print_board()


