import tkinter as tk
from tkinter import messagebox

from game_maker import PEG, EMPTY, get_english_board_cells


class PegSolitaireGUI:
    CELL_SIZE = 70      # pixel size of cells
    PEG_RADIUS = 22     # pixel radius of pegs

    def __init__(self, root, on_ok):
        self.root = root   
        self.on_ok = on_ok  

        self.root.title("Partial Peg Solitaire Unsolvability Checker")

        self.board_cells = get_english_board_cells()
        self.board_cells_set = set(self.board_cells)
        
        self.state = self.make_default_state()  # we always start in the classic start configuration
        
        self.marked_cells = set()

        # the actual 'canvas' where stuff is drawn
        self.canvas = tk.Canvas(
            root,
            width=7 * self.CELL_SIZE,
            height=7 * self.CELL_SIZE,
            bg="white",
            highlightthickness=0,   # border around canvas
        )
        self.canvas.pack(padx=20, pady=20) 

        self.canvas.bind("<Button-1>", self.handle_click)   # calls handle_clik on left mouse button click

        # frame for buttons, we can reuse this if we add more later (don't think it's necessary though)
        button_frame = tk.Frame(root)
        button_frame.pack(pady=(0, 20))

        # define the OK button
        ok_button = tk.Button(
            button_frame,
            text="OK",
            width=12,
            command=self.handle_ok,
        )
        ok_button.pack(side=tk.LEFT, padx=5)

        # define the RESET button
        reset_button = tk.Button(
            button_frame,
            text="RESET",
            width=12,
            command=self.reset_board,
        )
        reset_button.pack(side=tk.LEFT, padx=5)

        self.draw_board()

    def make_default_state(self):
        """
        This defines the standard start configuration of Peg Solitaire where all cells have a peg except the center one.
        This problem is solvable, so the unsolvability checker should NOT state that there is no solution!!
        """
        state = {}

        for cell in self.board_cells:
            if cell == (3, 3):
                state[cell] = EMPTY
            else:
                state[cell] = PEG

        return state

    def draw_board(self):
        """
        Draws the current state of the board onto the canvas, so it gets called after each mouse click for example
        """
        self.canvas.delete("all")   # remove everything currently drawn

        # go over all cells and see if they should be filled in
        for row in range(7):
            for col in range(7):
                cell = (row, col)

                if cell not in self.board_cells_set:    # skip invalid corner cells
                    continue

                # convert board coordinates into pixel coordinates to draw the cells and pegs
                x1 = col * self.CELL_SIZE
                y1 = row * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE

                cell_fill = "#fff4a3" if cell in self.marked_cells else "#ffffff"
                cell_outline = "#d62828" if cell in self.marked_cells else "#000000"
                cell_width = 4 if cell in self.marked_cells else 2

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=cell_fill,
                    outline=cell_outline,
                    width=cell_width,
                )

                # get center of the square
                center_x = x1 + self.CELL_SIZE // 2
                center_y = y1 + self.CELL_SIZE // 2

                if self.state[cell] == PEG:
                    fill = "#2f6fed"
                    outline = "#1d3f8f"
                else:
                    fill = "#939393"
                    outline = "#939393"

                self.canvas.create_oval(
                    center_x - self.PEG_RADIUS,
                    center_y - self.PEG_RADIUS,
                    center_x + self.PEG_RADIUS,
                    center_y + self.PEG_RADIUS,
                    fill=fill,
                    outline=outline,
                    width=2,
                )

    def handle_click(self, event):
        """
        Removes or adds a peg if we click on a cell 
        """
        col = event.x // self.CELL_SIZE
        row = event.y // self.CELL_SIZE
        cell = (row, col)

        if cell not in self.board_cells_set:
            return
        
        self.marked_cells = set()

        if self.state[cell] == PEG:
            self.state[cell] = EMPTY
        else:
            self.state[cell] = PEG

        self.draw_board()

    def handle_ok(self):
        """
        Checks that there was at least 1 peg selected and sends the current board config to main
        """
        peg_count = sum(
            1 for value in self.state.values()
            if value == PEG
        )

        if peg_count == 0:
            messagebox.showwarning(
                "You can't do that:",
                "Please select at least one peg!",
            )
            return

        self.on_ok(self.get_state())    # take the current state from the gui and give it to the OK function

    def get_state(self):
        """
        Returns the board state as a dictionary
        """
        return dict(self.state)

    def reset_board(self):
        self.state = self.make_default_state()
        self.marked_cells = set()
        self.draw_board()
        
    def show_marked_cells(self, marked_cells):
        """
        Show the cells that were marked by the unsolvability proof.
        """
        self.marked_cells = set(marked_cells)
        self.draw_board()

    def clear_marked_cells(self):
        """
        Removes all cell markings
        """
        self.marked_cells = set()
        self.draw_board()