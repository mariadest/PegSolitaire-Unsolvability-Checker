import tkinter as tk
from tkinter import messagebox

from gui import PegSolitaireGUI
from game_maker import get_english_board_cells,generate_operators,make_single_peg_goal
from peg_solitaire import PegSolitaireTask
from parity_unsolvability_1D import find_1d_unsolvability_proof
from resource_unsolvability import find_resource_unsolvability_proof

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


def handle_gui_check(gui, initial_state):
    task = build_task_from_gui_configuration(initial_state)

    print("Created a Peg Solitaire game!")
    print("Initial state:")
    print_state(task)

    # check for unsolvability with 1D features
    proof_1d = find_1d_unsolvability_proof(task)
    # check for unsolvability with resource counts 
    proof_resource = find_resource_unsolvability_proof(task)

    if proof_1d is not None:
        print("Unsolvability proof found with 1D features")
        print("Marked cells:", proof_1d["marked_cells"])
        print("-----------------------------------------------------")
        
        gui.show_marked_cells(proof_1d["marked_cells"])

        '''messagebox.showinfo(
            "We found a proof!",
            "An unsolvability proof was found using one-dimensional features over F2.",
        )''' 
        
        gui.status_label.config(text="An unsolvability proof was found using 1D features over F2! \n")
        
    elif proof_resource is not None:
        print("Unsolvability proof found with resource count")
        print("Initial resource:", proof_resource["initial_value"])
        print("Goal resource:", proof_resource["goal_value"])
        print("Positive cells:", proof_resource["positive_cells"])
        print("Negative cells:", proof_resource["negative_cells"])
        print("-----------------------------------------------------")

        gui.show_resource_cells(proof_resource["positive_cells"], proof_resource["negative_cells"], proof_resource["weights"])
        
        """ messagebox.showinfo(
            "We found a proof!",
            "An unsolvability proof was found using resource-count.\n\n"
            f"Initial resource: {proof_resource['initial_value']:.1f}\n"
            f"Goal resource: {proof_resource['goal_value']:.1f}",
        )"""
        
        gui.status_label.config(text="An unsolvability proof was found using resource count! \n"
                                f"Initial resource: {proof_resource['initial_value']:.1f}             Goal resource: {proof_resource['goal_value']:.1f}",)

    else:
        print("No unsolvability proof was found.")
        print("-----------------------------------------------------")

        '''messagebox.showinfo(
            "We failed.",
            "We could not find a proof. \n\n"
            "Guess you have to try for yourself :)",
        )'''
        
        gui.status_label.config(text="We could not find a proof. \n Time to find out yourself :)")

        
        gui.start_try_it_mode(show_message=False)
    
    

def main():
    root = tk.Tk()

    gui = PegSolitaireGUI(
        root=root,
        on_check=None,
    )
    
    def handle_check_from_gui(initial_state):
        handle_gui_check(gui, initial_state)

    gui.on_check = handle_check_from_gui

    root.mainloop()


if __name__ == "__main__":
    main()