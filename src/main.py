"""Runs the homework assignment step by step using a search algorithm
"""

import os
import os.path
from time import time

# helper function to deal with parsing the puzzle format
from formatter import board_from_file, generate_solution_file
# these are the CLI args, parsed
from args import args
# search algorithms
import search


# Step 1. Determine what search algorithm we are using
try:
    do_search = getattr(search, args.algorithm.lower())
except AttributeError:
    print(
        "Error! '{}' is not a search algorithm we have implemented".format(
            args.algorithm
        )
    )
    os._exit(1)  # janky

# Step 2. Read in the puzzle file
if not os.path.isfile(args.file):
    raise Exception('File `{0}` does not exist!'.format(args.file))

print('Reading file `{}` to solve.'.format(args.file))
with open(args.file, 'r') as file:
    contents = file.read()

print('\n=== PUZZLE FILE ===\n{}\n'.format(contents))

# Step 3. Build the initial state, called a `board`
board = board_from_file(contents)
print('+--- Initial Board ---+\n{}\n'.format(board))

# Step 4. Use the initial board to search for a solution (path) to the goal
start = time()
path = do_search(board)
end = time()
search.print_progress(done=True)

time_elapsed = end - start

# now convert to MICROseconds, time_elapsed is in seconds so * by 1,000,000
time_elapsed = int(round(time_elapsed * 1000000))

if not path:
    print("Error: Could not find a path!")
    os._exit(1)

# Step 5. Show the path (solution) we found
print('=== FOUND PATH ===')
step = 0
for board in path:
    print('''
+---- Step: {step} ----+
| Action: {action}   |
+-----------------+
{board}'''.format(
      step=step,
      board=board,
      action=board.parent_action.str_formatted()
      ))
    step += 1

solution_contents = generate_solution_file(path, time_elapsed)
print('\n=== SOLUTION ===\n{}'.format(solution_contents))

# Step 6. output the solution to a file so the TAs are happy
input_filename = os.path.basename(args.file)
solution_filename = input_filename \
    .replace('puzzle', 'solution') \
    .replace('Puzzle', 'Solution')

solution_dir = './solutions/'
solution_path = os.path.join(solution_dir, solution_filename)

print('\nWriting solution file `{}`'.format(solution_path))

if not os.path.exists(solution_dir):
    os.makedirs(solution_dir)

with open(solution_path, 'w+') as file:
    file.write(solution_contents)

print('Done!')
