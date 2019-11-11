Mingze Lin
email:m59lin@edu.uwaterloo.ca




Please note for 16 cities, the 

Run question2 versionA commandline:
python sudoku_versionA.py

Run question2 versionB commandline:
python sudoku_versionB.py

Run question2 versionC commandline:
python sudoku_versionC.py




matrix: 2d matrix that represent the board of Sudoku, matrix[y][x] is the block at (x,y)
var_matrix: 3d matrix that keep track of the available variable from domain for each matrix[y][x]

Version A:

backtrack_search:
Choose a coordinate (x1,y1), get one of the available variable from var_matrix[y1][x1], if it does not have conflict with the blocks on the same row, column 3x3 square, then choose either coordinate(x1+1, y1) or (0, y1+1) to do recursion. If (x1,y1) = (8,8), return True.
If recursion (child) failed and come back, choose the next available variable from var_matrix[y1][x1], if none available return False.
If recursion (child) succeed and come back, return True.

Version B:

backtrack_search:
Choose a coordinate (x1,y1), get one of the available variable from var_matrix[y1][x1], if it does not have conflict with the blocks on the same row, column 3x3 square, then do forward_check, if forward_check return true, then choose either coordinate(x1+1, y1) or (0, y1+1) to do recursion. If (x1,y1) = (8,8), return True.
If recursion (child) failed and come back, choose the next available variable from var_matrix[y1][x1], if none available return False.
If recursion (child) succeed and come back, return True.

forward_check:
Say the current block is matrix[y][x] with value V, for each of the blocks on the same row, column 3x3 square, reduce V from their respective var_matrix[yi][xi], return true as long as none of var_matrix[yi][xi] is reduced to empty list, otherwise undo reduce (call undo_forward_check).

Version C:

Heap: priority queue that ranks by the smallest length(var_matrix[y][x])
Heap will be changes whenever length(var_matrix[y][x]) is changed

backtrack_search:
Pop min from Heap (get the most restricted variable), if more than one has the same number of available variables, get the one that is affecting the most number white blocks by counting the number of white blocks on the same row, column 3x3 square (most constrained variable as tie breaker).
Count the occurrence of each number from domain on the same row, column 3x3 square, choose the least occurred value (least constraining value), if it does not have conflict with the blocks on the same row, column 3x3 square, then do forward_check, if forward_check return true, then pop another min from Heap. If heap is empty, return True.
If recursion (child) failed and come back, repeat.
If recursion (child) succeed and come back, return True.

forward_check:
Say the current block is matrix[y][x] with value V, for each of the blocks on the same row, column 3x3 square, reduce V from their respective var_matrix[yi][xi], return true as long as none of var_matrix[yi][xi] is reduced to empty list, otherwise undo reduce (call undo_forward_check).
