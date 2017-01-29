# Jacob Fischer's CS5400 Puzzle Solver

My solutions to the [CS5400 SP2017 puzzle assignment series][puzzle].

## Requirements

This is a Python 3 solution, so obviously you will need [Python 3][python] installed.

Aside from that there are no further dependencies.

## Usage

From the root of this repository run:

```
python3 ./src/main.py [ALGORITHM] [PUZZLE_FILE]
```

Where `[ALGORITHM]` is optional. It must be an algorithm implemented in the `src/algorithms.py` file.

At this time the options are:

* `bfts` - Beadth First Tree Search
* `bfgs` - Breadth First Graph Search _(default)_

And `[PUZZLE_FILE]` is also optional and should be a path to a properly formatted puzzle file.

If you want to pass a puzzle file, you must specificity the algorithm, as they are positional arguments.

## Solutions

After finding a solution to a puzzle, solutions are output in the `solutions/` directory automatically. The filename will be the original filename with any occurrences of `Puzzle` or `puzzle` replaced with `Solution` or `solution` respectively.

### Pre-solved

puzzles 1-3 were solved using BFS and the solutions are included in this repository. Feel free to re-run them as inputs to resolve them.

Puzzle 4 ate up too much RAM under BFGS so I killed it. Regardless it's not needed at this point as per TAs suggestions.

## Run file

A `run.sh` file is included as per assignment rules. It literally just does this:

```
python3 ./src/main.py bfts ./puzzles/puzzle1.txt
```

So it solves puzzle1 using Breadth First Tree Search.

## Terminology

Within the source code (`src/`) I refer to a few objects:

* `Board`: a container class that acts as a state for all the game objects. Some students called this a "Swamp". Board made more sense to me
* `Piece`: a game object within the `Board`.
* `Boat`: The specific Piece that is the Boat. Represented as a `B` with a directional arrow for its orientation
* `Tree`: A Cyprus tree. Represented with a `C#` where `#` is its index.
* `Turtle`: A turtle. Represented with a `T#` where `#` is its index.
* `Alligator`: An alligator. Represented with a `A#` where `#` is its index.
* `Goal`: where the boat must move to. Represented by a `G`, but may not show in board states if something is overlapping it.

## ASCII Boards

To help show what is visually happening I output my board states to a nice user friendly format. For example the examplePuzzle.txt's initial state looks like:

```
B- B> A0  .  .
 .  . A0  G  .
T0 T0 A0  .  .
 . T1 T1 C0  .
```

Notice the Boat has an arrow instead of an index (as there is always 1 boat).

## Other notes

The source should follow [PEP8][pep8] strictly. This means some lines of code are broken up on multiple lines a little oddly.

## Questions?

Just ask me.

[puzzle]: http://web.mst.edu/~tauritzd/courses/cs5400/sp2017/puzzle.html
[python]: https://www.python.org/
[pep8]: https://www.python.org/dev/peps/pep-0008/
