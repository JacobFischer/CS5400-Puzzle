import directions


def _action_character(action):
    """Transforms an Action into the character expected for the homework output
    For example, we say things can move forward and back, but the homework
    expects the direction they moved, plus all are single character
    representations

    Args:
        action (Action): The action you want the single character for
    Returns:
        str: a single character, either being 'U', 'L', 'D', 'R' for the
            direction it moved in, or 'C' or 'N' for clockwise and
            counterclockwise rotations of the boat respectively
    """
    if action.method == 'move_forward':
        return action.piece.orientation
    elif action.method == 'move_backward':
        return directions.invert(action.piece.orientation)
    elif action.method == 'rotate_clockwise':
        return 'C'
    else:  # action.method == 'rotate_counter_clockwise'
        return 'N'


class Action():
    """A simple container class to hold information about an action that
    changed a board state
    """

    def __init__(self, piece, method_str):
        """Creates an action

        Args:
            piece (Piece): the piece that this action is for
            method_str (str): the method name that the piece would invoke
        """
        self.board = piece.board
        self.piece = piece
        self.piece_name = piece.__class__.__name__  # for convenience
        self.piece_index = piece.index
        self.method = method_str

    def generate(self):
        """Generates the new Board that this Action represents

        Returns:
            Board: a new board where this action has been applied to
        """
        return self.board.__class__(self)  # note: this avoids cyclic reference

    def __repr__(self):
        """Returns the human readable string representation of the Action

        Returns:
            str: A human readable string (with method name, not action char)
        """
        return "Action<{self.piece_name}#{self.piece_index} {self.method}>" \
            .format(self=self)

    def str_formatted(self):
        """Returns the string formatted for homework output

        Returns:
            str: a string in the format '{class_letter} {index} {action}'
        """
        return '{class_letter} {index} {action}'.format(
            class_letter=self.piece_name[0],
            index=(self.piece_index or 0),
            action=_action_character(self)
        )
