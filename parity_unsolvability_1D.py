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

def solve_linear_system(A, b):
    """
    Solves A*w=b and return w.
    This is done over the field F2.
    """
    # convert into matrix and column vector over field F2
    A = GF(np.array(A))
    b = GF(np.array(b).reshape(-1, 1))

    R = np.concatenate([A, b], axis=1).row_reduce()
    num_cols = A.shape[1]

    # checks for contradictions (0 = 1) to see if the system of equations is unsolvable
    for row in R:
        left = row[:num_cols]   
        right = row[num_cols]   
        
        if np.all(left == 0) and right == 1:
            return None

    # Extract one solution. We set all free variables to 0.
    w = GF.Zeros(num_cols)
    for row in R:
        left = row[:num_cols]
        right = row[num_cols]
        nonzero_columns = np.nonzero(left)[0]

        if len(nonzero_columns) == 0:
            continue

        pivot_column = nonzero_columns[0]
        w[pivot_column] = right

    return w

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
    
    # do the actual solving
    w = solve_linear_system(A, b)
    
    # no solution was found, i.e. we don't have an unsolvability proof
    if w is None:
        return None
    
    # read out the marked_cells 
    marked_cells = []
    weights = {}
    for cell in cells:
        weight = int(w[index[cell]])
        weights[cell] = weight
        
        if weight == 1:
            marked_cells.append(cell)
    
    return {
        "method": "1d features",
        "marked_cells": marked_cells,
    }