EMPTY = 0
PEG = 1

from peg_solitaire import Operator, PegSolitaireTask

# ------------------------------- # 
#         BOARD DEFINITION        #
# ------------------------------- # 
# we currently only use the english board but we could also implement others
def get_english_board_cells():
    """
    This returns the cells of an english 7x7 Peg Solitaire board where the corners are left out like this:
    
    - - o o o - -
    - - o o o - -
    o o o o o o o
    o o o o o o o
    o o o o o o o
    - - o o o - -
    - - o o o - -
    
    A cell is speicifed as a tuple (row, col) ranging from 0 to 6
    """
    valid_cells = []

    for row in range(7):
        for col in range(7):
            # defines where we can have cells 
            in_top_left_corner = row < 2 and col < 2
            in_top_right_corner = row < 2 and col > 4
            in_bottom_left_corner = row > 4 and col < 2
            in_bottom_right_corner = row > 4 and col > 4

            # add all cells to valid_cells which are not in the corners
            if not (
                in_top_left_corner
                or in_top_right_corner
                or in_bottom_left_corner
                or in_bottom_right_corner
            ):
                valid_cells.append((row, col))

    return valid_cells


# ------------------------------- # 
#     MAKING INITIAL STATES       #
# ------------------------------- # 
# should be done over GUI at some point

# NOT NEEDED WITH GUI ANYMORE
def make_classic_initial_state():
    """
    This defines the standard start configuration of Peg Solitaire where all cells have a peg except the center one.
    This problem is solvable, so the unsolvability checker should NOT state that there is no solution!!
    """
    board_cells = get_english_board_cells()
    state = {}

    for cell in board_cells:
        if cell == (3, 3):
            state[cell] = EMPTY
        else:
            state[cell] = PEG

    return state

# ---------------------- # 
#      DEFINE GOAL       #
# ---------------------- # 
def make_single_peg_goal(goal_cell):
    """
    Defines a concrete goal state where exactly one peg remains at 'goal_cell'
    """
    board_cells = get_english_board_cells()
    goal_state = {}

    for cell in board_cells:
        if cell == goal_cell:
            goal_state[cell] = PEG
        else:
            goal_state[cell] = EMPTY

    return goal_state
    
def make_all_single_peg_goals():
    """
    Defines all possible goal states where exactly one peg remains
    """
    board_cells = get_english_board_cells()
    goal_states = []

    for goal_cell in board_cells:
        goal_state = make_single_peg_goal(goal_cell)
        goal_states.append(goal_state)

    return goal_states

# ------------------------------- # 
#         DEFINE OPERATORS        #
# ------------------------------- # 
# nothing should be changed here unless we want to change the rules of Peg Solitaire
def generate_operators(board_cells):
    """
    Generates the operators for all possible moves in peg solitaires.
    """
    
    # in which direction a peg can jump
    directions = [
        (1, 0),   # down
        (-1, 0),  # up
        (0, 1),   # right
        (0, -1),  # left
    ]

    board_cells_set = set(board_cells)
    operators = []

    # adds an operator for every possible jump on the board, going cell by cell
    for row, col in board_cells:
        for d_row, d_col in directions:
            from_cell = (row, col)
            over_cell = (row + d_row, col + d_col)
            to_cell = (row + 2 * d_row, col + 2 * d_col)

            # check that all cells are actually valid cells and then add the operator
            if over_cell in board_cells_set and to_cell in board_cells_set:
                name = f"jump_{from_cell}_over_{over_cell}_to_{to_cell}"

                pre = {
                    from_cell: PEG,
                    over_cell: PEG,
                    to_cell: EMPTY,
                }

                eff = {
                    from_cell: EMPTY,
                    over_cell: EMPTY,
                    to_cell: PEG,
                }

                operators.append(Operator(name, pre, eff))

    return operators


def build_classic_task(goal_cell=(3, 3)):
    """
    Build the full planning task for classic Peg Solitaire.
    """
    board_cells = get_english_board_cells()
    operators = generate_operators(board_cells)
    initial_state = make_classic_initial_state()
    goal_state = make_single_peg_goal(goal_cell)

    return PegSolitaireTask(
        board_cells=board_cells,
        operators=operators,
        initial_state=initial_state,
        goal_state=goal_state,
    )