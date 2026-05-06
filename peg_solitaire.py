class Operator:
    def __init__(self, name, pre, eff):
        self.name = name
        self.pre = pre
        self.eff = eff

    # prints out an operator (mainly used for debugging)
    def __repr__(self):
        return f"Operator: name={self.name}, pre={self.pre}, eff={self.eff}"


class PegSolitaireTask:
    def __init__(self, board_cells, operators, initial_state, goal_state):
        self.board_cells = board_cells
        self.operators = operators
        self.initial_state = initial_state
        self.goal_state = goal_state
