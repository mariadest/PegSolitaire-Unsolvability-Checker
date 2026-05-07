class Operator:
    def __init__(self, name, pre, eff):
        self.name = name
        self.pre = pre
        self.eff = eff


class PegSolitaireTask:
    def __init__(self, board_cells, operators, initial_state, goal_state):
        self.board_cells = board_cells
        self.operators = operators
        self.initial_state = initial_state
        self.goal_state = goal_state
