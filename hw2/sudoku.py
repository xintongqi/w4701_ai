#!/usr/bin/env python
# coding: utf-8

# In[1]:


# !/usr/bin/env python
# coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import time

import numpy as np

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def get_row(var):
    row = var[0]
    rows = []
    for i in range(9):
        r = chr(ord("1") + i)
        rows.append(row + r)
    return rows


def get_col(var):
    col = var[1]
    cols = []
    for i in range(9):
        c = chr(ord("A") + i)
        cols.append(c + col)
    return cols


def get_mini_grid(var):
    mini_grids = {
        "00": ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'],
        "01": ['A4', 'A5', 'A6', 'B4', 'B5', 'B6', 'C4', 'C5', 'C6'],
        "02": ['A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9'],
        "10": ['D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2', 'F3'],
        "11": ['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6'],
        "12": ['D7', 'D8', 'D9', 'E7', 'E8', 'E9', 'F7', 'F8', 'F9'],
        "20": ['G1', 'G2', 'G3', 'H1', 'H2', 'H3', 'I1', 'I2', 'I3'],
        "21": ['G4', 'G5', 'G6', 'H4', 'H5', 'H6', 'I4', 'I5', 'I6'],
        "22": ['G7', 'G8', 'G9', 'H7', 'H8', 'H9', 'I7', 'I8', 'I9']}
    row = (ord(var[0]) - ord('A')) // 3
    col = (ord(var[1]) - ord('1')) // 3
    return mini_grids[str(row) + str(col)]


def get_neighbors(var):
    row_n = set(get_row(var))
    col_n = set(get_col(var))
    mini_grid_n = set(get_mini_grid(var))
    n = row_n | col_n | mini_grid_n
    n.remove(var)
    return n


def select_var_mrv(assignment, domains):
    min_domain_len = 100
    var = None

    for k, v in assignment.items():
        if v == 0 and len(domains[k]) < min_domain_len:
            min_domain_len = len(domains[k])
            var = k

    return var


def is_safe(value, var, assignment, neighbors):
    neighbor = neighbors[var]
    for n in neighbor:
        if assignment[n] == value:
            return False

    return True


def forward_checking(neighbors, domains, var, val):
    for neighbor in neighbors[var]:
        if val in domains[neighbor]:
            domains[neighbor].remove(val)
            if len(domains[neighbor]) == 0:
                return False

    return True


def restore_domains(domains, val, var, neighbors):
    for neighbor in neighbors[var]:
        domains[neighbor].add(val)


def backtrack(assignment, neighbors, domains):
    var = select_var_mrv(assignment, domains)

    if var is None:
        return True

    domain = list(domains[var])

    for v in domain:
        if v not in domains[var]:  # modifying domain while looping, the item might be gone
            continue

        if is_safe(v, var, assignment, neighbors):
            assignment[var] = v
            fc_success = forward_checking(neighbors, domains, var, v)

            if fc_success:
                backtrack_success = backtrack(assignment, neighbors, domains)
                if backtrack_success:
                    return True
                else:
                    assignment[var] = 0
                    restore_domains(domains, v, var, neighbors)
            else:
                assignment[var] = 0
                restore_domains(domains, v, var, neighbors)

    return False


def backtracking(board):
    """Takes a board and returns solved board."""
    assignment = dict(board)

    neighbors = dict(board)
    for k in neighbors:
        neighbors[k] = get_neighbors(k)

    domains = dict(board)
    for k in domains:
        domains[k] = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    # forward checking beforehand
    for var, v in board.items():
        if v != 0:
            forward_checking(neighbors, domains, var, v)

    state = backtrack(assignment, neighbors, domains)

    if state:
        return assignment
    else:
        return "Failed to solve this board"


if __name__ == '__main__':
    if len(sys.argv) > 1:

        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = {ROW[r] + COL[c]: int(sys.argv[1][9 * r + c])
                 for r in range(9) for c in range(9)}

        solved_board = backtracking(board)

        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Setup readme
        readme_filename = 'README.txt'
        readme = open(readme_filename, "w")

        # Keep track of runtime
        runtime = list()

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = {ROW[r] + COL[c]: int(line[9 * r + c])
                     for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            # print_board(board)

            start_time = time.time()
            # Solve with backtracking
            solved_board = backtracking(board)
            end_time = time.time()
            runtime.append(end_time - start_time)

            # Print solved board. TODO: Comment this out when timing runs.
            # print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        print("Finishing all boards in file.")

        # Calculate min max avg and std of runtime
        runtime_np = np.array(runtime)
        readme.write("Number of boards solved " + str(len(runtime)) + "\n")
        readme.write("Min of runtime: " + str(np.min(runtime_np)) + "\n")
        readme.write("Max of runtime: " + str(np.max(runtime_np)) + "\n")
        readme.write("Mean of runtime: " + str(np.mean(runtime_np)) + "\n")
        readme.write("Standard deviation of runtime: " + str(np.std(runtime_np)) + "\n")
