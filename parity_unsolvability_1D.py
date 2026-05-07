import numpy as np
import galois


GF = galois.GF(2)   # field F2

def make_vector(cells, index, n):
    """
    Gives us back a vector containing an entry for each cell in the puzzle.
    If the specific cell is included in 'cells' the value is 1, if it is not it's 0.
    """
    vector = np.zeros(n, dtype=int)
    for cell in cells:
        vector[index[cell]] = 1
    return GF(vector)

def find_1d_unsolvability_proof(task):
    """
    Finds a weight function w for the separating function.
    The basic idea is we "mark" cells, i.e. the weight function assigns them a value of 1. Unmarked cells are 0.
    The goal is to find an assignment of marked cells whose parity proves that the puzzle is unsolvable.
    """
    cells = task.board_cells
    n = len(cells)
    
    # Assign every cell a number so we can work with cells in a 1D array/vector using indexes.
    index = {}
    for i, cell in enumerate(cells):
        index[cell] = i
        
    A = []
        
    # initial and goal state differ in parity (corresponds to (6)) 
    differing_cells = []
    for cell in cells:
        if task.initial_state[cell] != task.goal_state[cell]:
            differing_cells.append(cell)
    A.append(make_vector(differing_cells, index, n))  

    # every operator application preserves parity (corresponds to (8))
    for operator in task.operators:
        updated_cells = operator.pre.keys()
        A.append(make_vector(updated_cells, index, n))
    
    b = [0] * len(A)
    b[0] = 1    # the first equation should equal to 1 instead of 0, i.e. parity of initial and goal state differ (as defined in (6))
    
    # actually find w