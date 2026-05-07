import tkinter as tk

from gui import PegSolitaireGUI
from game_maker import (
    get_english_board_cells,
    generate_operators,
    make_single_peg_goal,
)
from peg_solitaire import PegSolitaireTask


def build_task_from_gui_configuration(initial_state, goal_cell=(3, 3)):
    """
    Builds a PegSolitaireTask from the configuration selected in the GUI.
    We use the middle cell as a goal cell here
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


def handle_gui_ok(initial_state):
    task = build_task_from_gui_configuration(initial_state)

    print("Created a Peg Solitaire game!")
    print("Initial state:")
    print_state(task)

    # here the actual unsolvability check should happen
    # ...


def main():
    root = tk.Tk()

    PegSolitaireGUI(
        root=root,
        on_ok=handle_gui_ok,
    )

    root.mainloop()


if __name__ == "__main__":
    main()