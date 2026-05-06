from game_maker import build_classic_task, PEG, EMPTY

task = build_classic_task()

print("Number of board cells:", len(task.board_cells))
print("Number of operators:", len(task.operators))

print("Initial state:")
for row in range(7):
    line = ""
    for col in range(7):
        cell = (row, col)

        if cell not in task.board_cells:
            line += "  "
        elif task.initial_state[cell] == PEG:
            line += "O "
        else:
            line += ". "
    print(line)

print("\nFirst 5 operators:")
for op in task.operators[:5]:
    print(op)