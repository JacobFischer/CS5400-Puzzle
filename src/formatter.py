"""A collection of function used to parse to and from the file formatted as
described by the homework
"""

from pieces import Piece, Alligator, Turtle, Tree, Boat, Goal
from board import Board
from point import Point
import directions


def board_from_file(file_contents):
    """Parsed the contents of a file to a board state
    Yes the file format is stupid, whatever. Have fun with the massive if/else

    Args:
        contents (string): the contents of a puzzle file.
            Must be in the correct format
    """
    board = Board()

    for line in file_contents.splitlines():
        split = line.split()
        # each line will always be 3 things, two numbers, followed by an
        # optional letter
        first = int(split[0])
        second = int(split[1])
        third = split[2] if len(split) == 3 else None

        # 1st line, so record the width/height
        if board.width is None:
            board.width = first
            board.height = second

        # 2nd line, so record the rad source
        elif board.radiation_source is None:
            board.radiation_source = Point(first, second)

        # 3rd line, which is rad mag followed by decay
        elif board.radition_magnitude is None:
            board.radition_magnitude = first
            board.radition_decay = second

        # 4th line, which is the number of alligators, turtles, & trees
        elif board.alligators is None:
            board.alligators = [None] * first
            board.turtles = [None] * second
            # `third` is actually an integer here (number of trees)
            board.trees = [None] * int(third)

        # 5th+ lines, we are recoding alligators
        elif None in board.alligators:
            index = board.alligators.index(None)
            board.alligators[index] = Alligator(
                board=board,
                index=index,
                x=first,
                y=second,
                orientation=third
            )

        # 5th+ lines, we are recoding turtles
        elif None in board.turtles:
            # we are recording turtles
            index = board.turtles.index(None)
            board.turtles[index] = Turtle(
                board=board,
                index=index,
                x=first,
                y=second,
                orientation=third
            )

        # 5th+ lines, we are recoding trees
        elif None in board.trees:
            index = board.trees.index(None)
            board.trees[index] = Tree(
                board=board,
                index=index,
                x=first,
                y=second
            )

        # second to last line, the boat
        elif board.boat is None:
            board.boat = Boat(
                board=board,
                x=first,
                y=second,
                orientation=third
            )

        # last line, the goal point
        elif board.goal is None:
            board.goal = Goal(
                board=board,
                x=first,
                y=second
            )

        # else: shouldn't happen, or blank line(s) at the end of the file

    board.update()

    return board


def file_from_board(board):
    """Create the file format from a board state

    Args:
        board (Board): the board to build the file formatted str for

    Returns:
        str: a string ready to put into a file formatted in the homework's spec
    """
    return """{board.width} {board.height}
{board.radiation_source.x} {board.radiation_source.y}
{board.radition_magnitude} {board.radition_decay}
{num_alligators} {num_turtles} {num_trees}{alligators}{turtles}{trees}
{board.boat.pivot.x} {board.boat.pivot.y} {board.boat.orientation}
{board.goal.pivot.x} {board.goal.pivot.y}""".format(
        board=board,
        num_alligators=len(board.alligators),
        num_turtles=len(board.turtles),
        num_trees=len(board.trees),
        alligators=''.join([
            '\n{a.pivot.x} {a.pivot.y} {a.orientation}'.format(a=alligator)
            for alligator in board.alligators
        ]),
        turtles=''.join([
            '\n{t.pivot.x} {t.pivot.y} {t.orientation}'.format(t=turtle)
            for turtle in board.turtles
        ]),
        trees=''.join([
            '\n{t.pivot.x} {t.pivot.y}'.format(t=tree)
            for tree in board.trees
        ])
    )


def generate_solution_file(path, time):
    """Create the solution file format from a path of boards

    Args:
        path (list[Board]): A list of boards starting with the first modified
        board state (not the initial board), and ending in the final (goal)
        state

    Returns:
        str: a string ready to put into a solution file as per the homework
    """
    return """{time}
{final_board.boat.radiation}
{len_path}
{path}
{board_as_file}""".format(
        time=time,
        final_board=path[-1],
        len_path=len(path),
        path=','.join([board.parent_action.str_formatted() for board in path]),
        board_as_file=file_from_board(path[-1])
    )
