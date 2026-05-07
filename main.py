import tkinter as tk
from tkinter import messagebox

from gui import PegSolitaireGUI
from game_maker import get_english_board_cells,generate_operators,make_single_peg_goal
from peg_solitaire import PegSolitaireTask
from parity_unsolvability_1D import find_1d_unsolvability_proof

def build_task_from_gui_configuration(initial_state, goal_cell=(3, 3)):
    """
    Builds a PegSolitaireTask from the configuration selected in the GUI.
    We use the middle cell as a goal cell here.
    """
    board_cells = get_english_board_cells()
    operators = generate_operators(board_cells)
    goal_state = make_single_peg_goal(goal_cell)

    return PegSolitaireTask(
        board_cells=board_cells,
        operators=operators,
        initial_state=initial_state,
        goal_state=goal_state,
    )

# TODO: make an option where we don't have to end with the peg in the middle cell but ANY cell
# TODO: make an option where we can choose where the last peg should be


def print_state(task):
    
    # print out what the board looks like (mainly for debugging, not really needed)
    for row in range(7):
        line = ""

        for col in range(7):
            cell = (row, col)

            if cell not in task.board_cells:
                line += "  "
            elif task.initial_state[cell] == 1:
                line += "O "
            else:
                line += ". "

        print(line)


def handle_gui_ok(initial_state):
    task = build_task_from_gui_configuration(initial_state)

    print("Created a Peg Solitaire game!")
    print("Initial state:")
    print_state(task)

    # check for unsolvability with 1D features
    '''proof_1d = find_1d_unsolvability_proof(task)

    if proof_1d is not None:
        print("Unsolvability proof found with one-dimensional F_2 features!")
        print("Marked cells:", proof_1d["marked_cells"])

        messagebox.showinfo(
            "We found a proof!",
            "An unsolvability proof was found using one-dimensional parity features :) / :(",
        )
    else:
        messagebox.showinfo(
            "We failed.",
            "No proof for unsolvability has been found, time to try for yourself (>ᴗ•)!",
        )'''

    # TODO: check for unsolvability with 2D features
    
    
    # TODO (optional): include Beasley argument checks


def main():
    root = tk.Tk()

    PegSolitaireGUI(
        root=root,
        on_ok=handle_gui_ok,
    )

    root.mainloop()


if __name__ == "__main__":
    main()