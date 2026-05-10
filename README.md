# The (Partial) Peg Solitaire Unsolvability Checker 
## About
This project allows users to test an initial Peg Solitaire configuration for unsolvability.   
The project itself tries two different approaches to find an unsolvability proof:  
1. Find a separating function based on one-dimensional features over the field F2.  
This is based on the separating functions framework by Christen et al. in *Detecting Unsolvability Based on Separating Functions* (2022).
2. Use a resource-count approach where weights are assigned to cells.  
This is based on Chapter 5 of *The Ins and Outs of Peg Solitaire* (1985) by J. D. Beasley.

This approach might not recognize all unsolvable instances. If we don't find a proof it does **not** follow that the puzzle is actually solvable.

## How to Start
The project is run in Python. It was tested with Python 3.10.11.  
The needed dependencies are defined in `dependencies.txt`. They can be installed with:
```bash
pip install -r dependencies.txt
```
The project uses `tkinter` from Python's standard library. However, for some Linux systems (e.g. Ubuntu) it may not be automatically included and needs to be installed separately.  

The project can be started with:
```bash
python main.py
````
or: 
```bash
python3 main.py
```

## How to Use
We always start in the classic English Peg Solitaire initial configuration where one Peg is missing in the middle (insert image). The goal is to end up with a single peg in the middle hole (position (3, 3)).  
<img src="imgs/classic_initial_config.png" alt="middle hole" width="300">

### Setup  
By clicking on a peg we remove it. Clicking on a hole adds a peg. With the `Clear Board` button we can remove all pegs. With `Reset Board` we go back to the classic initial configuration.

### Finding a Proof
If we are happy with our initial configuration we can press `Check`, this searches for an unsolvability proof. There are three possible outcomes:  
- **We find a proof using 1d features over F2**.  
The highlighted cells are the ones the weight function assigns a value of 1, i.e. the cells whose parity we are looking at.  
<img src="imgs/unsolvable_1d.png" alt="middle hole" width="300">

- **We find a proof using the resource-count based approach**.  
The cells highlighted in green are the ones that get assigned a positive weight, the red cells get assigned a negative weight. Cells without a highlight have a weight of 0. The weights are also specified in each cell.  
<img src="imgs/unsolvable_count.png" alt="middle hole" width="300">
- **We cannot find a proof**.  
In this case we enter the *TRY IT* mode where the user can play Peg Solitaire starting from the given position. While playing we can use the `Check` button to check if we can still not find an unsolvability proof for the current position. If we do we either caused ourselves to end up in an unsolvable position or the previous position was in fact actually unsolvable. *TRY IT* mode can be deactivated by pressing the `Stop Trying` button.
