# resource_unsolvability_1D.py

import numpy as np
from scipy.optimize import linprog


PEG = 1
EMPTY = 0


def state_resource_value(state, weights):
    """
    Computes the resource value of the state, i.e. sums up the values of cells where we have a peg (empty cells are ignored)
    """
    return sum(
        weights[cell]
        for cell, value in state.items()
        if value == PEG
    )


def create_operator_coefficients(operator, index, n):
    """
    Turns a Peg Solitaire move into a coefficient vector.
    The vector contains a -1 in cells the peg has come from and has jumped over and a +1 in the cell it landed in.
    The rest is filled with 0's.
    """
    coeffs = np.zeros(n)

    mentioned_cells = set(operator.pre.keys()) | set(operator.eff.keys())   # get cells mentioned in the move

    # compared values before and after the move and writes difference in the vector
    for cell in mentioned_cells:
        before = operator.pre.get(cell)
        after = operator.eff.get(cell)

        coeffs[index[cell]] = after - before

    return coeffs


def find_resource_unsolvability_proof(task, epsilon=1.0):
    """
    Finds a one-dimensional real-valued resource-count proof.

    We look for cell weights w such that:

        resource(after) <= resource(before)

    for every operator, and:

        resource(goal) >= resource(initial) + epsilon

    If such weights exist, the goal cannot be reachable from the initial state.
    """
    cells = task.board_cells
    n = len(cells)

    index = {}

    for i, cell in enumerate(cells):
        index[cell] = i

    A = []
    b = []

    # create the inequalities
    for operator in task.operators:
        A.append(create_operator_coefficients(operator, index, n))
        b.append(0.0)  


    # Here we separate the initial state from the goal state
    # We need 'initial_state - goal_state < 0'.
    # BUT: as we cannot use < in LP we use 'initial_state - goal_state <= -1'
    separation = np.zeros(n)

    for cell in cells:
        separation[index[cell]] = (
            task.initial_state[cell] - task.goal_state[cell]
        )

    A.append(separation)
    b.append(-1)

    # We only care about whether there is a solution or not, so we use a 0 objective; basically we say "minimize 0".
    objective = np.zeros(n)

    result = linprog(
        c=np.zeros(n),      # we only care about if there is a solution or not; here we "minimize 0"
        A_ub=np.array(A),
        b_ub=np.array(b),
        bounds=[(None, None)] * n,
        method="highs",
    )

    if not result.success:
        return None

    weights_vector = result.x
    # get a dictionary of cells and their weights
    weights = {}
    for cell in cells:
        cell_index = index[cell]
        weight = weights_vector[cell_index]
        weights[cell] = float(weight)

    # collect values of initial and goal state 
    initial_value = state_resource_value(task.initial_state, weights)
    goal_value = state_resource_value(task.goal_state, weights)
    
    # get all cells with a positive and a negative weight
    positive_cells = [cell for cell, weight in weights.items() if weight > 1e-8]
    negative_cells = [cell for cell, weight in weights.items() if weight < -1e-8]

    return {
        "method": "1d resource count",
        "weights": weights,
        "positive_cells": positive_cells,
        "negative_cells": negative_cells,
        "initial_value": initial_value,
        "goal_value": goal_value,
    }