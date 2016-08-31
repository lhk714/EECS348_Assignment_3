import ref
execfile("ref.py")
sb = ref.init_board("input_puzzles/easy/4_4.sudoku")
sb = ref.solve(sb, True, True, False, True)  #BT
sb.print_board()
