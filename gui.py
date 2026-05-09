import tkinter as tk
from tkinter import messagebox

from game_maker import PEG, EMPTY, get_english_board_cells


class PegSolitaireGUI:
    CELL_SIZE = 70      # pixel size of cells
    PEG_RADIUS = 22     # pixel radius of pegs

    def __init__(self, root, on_check):
        self.root = root   
        self.on_check = on_check  

        self.root.title("The (Partial) Peg Solitaire Unsolvability Checker")

        self.board_cells = get_english_board_cells()
        self.board_cells_set = set(self.board_cells)
        
        self.state = self.make_default_state()  # we always start in the classic start configuration
        
        self.marked_cells = set()
        self.positive_cells = set()
        self.negative_cells = set()
        self.resource_weights = {}
        
        self.play_mode = False
        self.selected_cell = None

        # the actual 'canvas' where stuff is drawn
        self.canvas = tk.Canvas(
            root,
            width=7 * self.CELL_SIZE,
            height=7 * self.CELL_SIZE,
            bg="#f4f6f8",
            highlightthickness=0,   # border around canvas
        )
        self.canvas.pack(padx=20, pady=20) 

        self.canvas.bind("<Button-1>", self.handle_click)   # calls handle_clik on left mouse button click

        # frame for buttons, we can reuse this if we add more later (don't think it's necessary though)
        button_frame = tk.Frame(root)
        button_frame.pack(pady=(0, 20))

        # define the CHECK button
        check_button = tk.Button(
            button_frame,
            text="Check",
            width=12,
            command=self.handle_check,
        )
        check_button.pack(side=tk.LEFT, padx=5)

        # define the RESET button
        reset_button = tk.Button(
            button_frame,
            text="Reset Board",
            width=12,
            command=self.reset_board,
        )
        reset_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = tk.Button(
            button_frame,
            text="Clear Board",
            width=12,
            command=self.clear_board,
        )
        
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_trying_button = tk.Button(
            button_frame,
            text="Stop Trying",
            width=12,
            command=self.stop_try_it_mode,
            state=tk.DISABLED,
        )
        self.stop_trying_button.pack(side=tk.LEFT, padx=5)

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

                if cell == self.selected_cell:
                    cell_fill = "#b0ceef"
                    cell_outline = "#1f91b4"
                    cell_width = 4
                elif cell in self.positive_cells:
                    cell_fill = "#b6ffcf"      # yellow
                    cell_outline = "#2f8f57"   # red
                    cell_width = 4
                elif cell in self.negative_cells:
                    cell_fill = "#ffb9b9"      # light blue
                    cell_outline = "#b33a3a"   # dark blue
                    cell_width = 4
                elif cell in self.marked_cells:
                    cell_fill = "#fff3bf"
                    cell_outline = "#c49a00"
                    cell_width = 4
                else:
                    cell_fill = "#fdfdfd"
                    cell_outline = "#000000"
                    cell_width = 2

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
                
                # Show the resource-count weights in the cells (if there are some)
                if cell in self.resource_weights:
                    weight = self.resource_weights[cell]
                    self.canvas.create_text(
                        center_x,
                        center_y,
                        text=self.format_weight(weight),
                        anchor="center",
                        fill="#000000",
                        font=("Arial", 12, "bold"),
                    )

    def handle_click(self, event):
        """
        In setup mode: removes or adds a peg if we click on a cell.
        In play mode: lets the user play Peg Solitaire.
        """
        self.clear_marked_cells()
        
        col = event.x // self.CELL_SIZE
        row = event.y // self.CELL_SIZE
        cell = (row, col)

        if cell not in self.board_cells_set:
            return

        if self.play_mode:
            self.handle_play_click(cell)
            return

        # setup mode
        self.marked_cells = set()

        if self.state[cell] == PEG:
            self.state[cell] = EMPTY
        else:
            self.state[cell] = PEG

        self.draw_board()

    def handle_check(self):
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
                "This is just an empty board and not a game.",
            )
            return

        self.on_check(self.get_state())    # take the current state from the gui and give it to the CHECK function

    def get_state(self):
        """
        Returns the board state as a dictionary
        """
        return dict(self.state)

    def reset_board(self):
        """
        resets everything back to the initial state and sets TRY IT mode off
        """
        self.state = self.make_default_state()
        self.marked_cells = set()
        self.positive_cells = set()
        self.negative_cells = set()
        self.resource_weights = {}
        self.play_mode = False
        self.selected_cell = None
        self.disable_stop_trying()
        self.draw_board()
        
    def show_marked_cells(self, marked_cells):
        """
        highlights marked cells
        """
        self.marked_cells = set(marked_cells)
        self.draw_board()
        
    def show_resource_cells(self, positive_cells, negative_cells, weights):
        """
        highlights positive and negative cells 
        """
        self.marked_cells = set()
        self.positive_cells = set(positive_cells)
        self.negative_cells = set(negative_cells)
        
        # draw non-zero weights
        self.resource_weights = {}
        for cell, weight in weights.items():
            if abs(weight) > 1e-8:
                self.resource_weights[cell] = weight
                
        self.draw_board()

    def clear_marked_cells(self):
        """
        Removes all cell markings
        """
        self.marked_cells = set()
        self.positive_cells = set()
        self.negative_cells = set()
        self.resource_weights = {}
        self.draw_board()
        
    
    # ----------------------------- #
    #   functions for TRY IT mode   #
    # ----------------------------- #
    def enable_stop_trying(self):
        """
        Enables the STOP TRYING button while in TRY IT mode
        """
        self.stop_trying_button.config(state=tk.NORMAL)

    def disable_stop_trying(self):
        """
        Disables the STOP TRYING button outside TRY IT mode
        """
        self.stop_trying_button.config(state=tk.DISABLED)


    def start_try_it_mode(self, show_message=True):
        """
        Starts playable Peg Solitaire mode.
        """
        self.play_mode = True
        self.selected_cell = None
        self.marked_cells = set()
        self.positive_cells = set()
        self.negative_cells = set()
        self.resource_weights = {}
        self.enable_stop_trying()
        self.draw_board()

        if show_message:
            messagebox.showinfo(
                "Try it!",
                "You can now play Peg Solitaire. Good luck in finding a solution! \n\n"
                "(If there is one)"
            )


    def handle_play_click(self, cell):
        """
        Handles clicks while in TRY IT mode
        """
        # First click: select a peg
        if self.selected_cell is None:
            if self.state[cell] == PEG:
                self.selected_cell = cell
                self.draw_board()
            return

        # Clicking the selected peg again deselects it
        if cell == self.selected_cell:
            self.selected_cell = None
            self.draw_board()
            return

        # Second click: choose cell to move to
        from_cell = self.selected_cell
        to_cell = cell

        if self.is_valid_move(from_cell, to_cell):
            self.apply_move(from_cell, to_cell)
            self.selected_cell = None
            self.draw_board()
            self.check_game_end()
        else:
            self.selected_cell = None
            self.draw_board()


    def is_valid_move(self, from_cell, to_cell):
        """
        Checks if the move we want to do is legal
        """
        if self.state[from_cell] != PEG:
            return False

        if self.state[to_cell] != EMPTY:
            return False

        from_row, from_col = from_cell
        to_row, to_col = to_cell

        row_diff = to_row - from_row
        col_diff = to_col - from_col

        # Move must be exactly two cells horizontally or vertically
        valid_vertical_jump = abs(row_diff) == 2 and col_diff == 0
        valid_horizontal_jump = abs(col_diff) == 2 and row_diff == 0

        if not (valid_vertical_jump or valid_horizontal_jump):
            return False

        jumped_cell = (
            from_row + row_diff // 2,
            from_col + col_diff // 2,
        )

        if jumped_cell not in self.board_cells_set:
            return False

        if self.state[jumped_cell] != PEG:
            return False

        return True


    def apply_move(self, from_cell, to_cell):
        """
        Applies a valid Peg Solitaire move, i.e. the peg jumps and the jumped over one gets removed
        """
        from_row, from_col = from_cell
        to_row, to_col = to_cell

        jumped_cell = (
            from_row + (to_row - from_row) // 2,
            from_col + (to_col - from_col) // 2,
        )

        self.state[from_cell] = EMPTY
        self.state[jumped_cell] = EMPTY
        self.state[to_cell] = PEG


    def check_game_end(self):
        """
        Checks whether the game has ended.
        """
        peg_cells = [
            cell for cell, value in self.state.items()
            if value == PEG
        ]

        # Game only ends when there is one peg left
        if len(peg_cells) == 1:
            final_cell = peg_cells[0]

            if final_cell == (3, 3):
                messagebox.showinfo(
                    "Congratulation!",
                    "You found a solution!",
                )
            else:
                messagebox.showinfo(
                    "Congratulation?",
                    "You ended up with one Peg! \n\n"
                    "But it's not in the correct position :/"
                )

            self.play_mode = False
            self.selected_cell = None
            self.disable_stop_trying()
            self.draw_board()
            
            
    def stop_try_it_mode(self):
        """
        Returns to regular mode
        """
        self.play_mode = False
        self.selected_cell = None
        self.disable_stop_trying()
        self.draw_board()
        
    def format_weight(self, weight):
        """
        Format the weights of resource count to then display them on the board.
        We keep 1 decimal place, otherwise it gets very clutterd.
        """
        # round when there are very very small differences
        if abs(weight) < 1e-10:
            return "0"
        if abs(weight - round(weight)) < 1e-10:
            return str(int(round(weight)))

        return f"{weight:.1f}"
    
    def clear_board(self):
        for cell in self.board_cells:
            self.state[cell] = EMPTY

        self.marked_cells = set()
        self.positive_cells = set()
        self.negative_cells = set()
        self.resource_weights = {}
        self.play_mode = False
        self.selected_cell = None
        self.disable_stop_trying()
        self.draw_board()