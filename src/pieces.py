from point import Point
from action import Action
import directions


class Piece:
    """An object on a game board (base class)"""

    length = 1

    def __init__(self, board=None, index=None, x=-1, y=-1,
                 orientation=None, original=None):
        self.board = board
        self.index = index
        self.pivot = Point(x, y)
        self.orientation = orientation

        if original:  # then clone it!
            self._copy_from(original)

    def _copy_from(self, original):
        self.index = original.index
        self.pivot = Point(original.pivot.x, original.pivot.y)
        self.orientation = original.orientation

    def at(self, x, y=None):
        if y is None:
            y = x.y
            x = x.x

        front = self.front()

        return (self.pivot.x <= x <= front.x and
                self.pivot.y <= y <= front.y) or (
                front.x <= x <= self.pivot.x and
                front.y <= y <= self.pivot.y)

    def front(self):
        return directions.offset(
            self.pivot, self.orientation, self.__class__.length-1
        )

    def clone(self, board=None):
        return self.__class__(board=board, original=self)

    def get_actions(self):
        return []

    def __repr__(self):
        return "{name} {pt}{dir}".format(
            name=self.__class__.__name__,
            pt=self.pivot,
            dir='' if self.orientation is None else " " + self.orientation
        )


class Tree(Piece):
    pass


class Goal(Piece):
    pass


class MoveForwardPiece(Piece):
    length = 2  # all things that can move forward are at least 2 long

    def can_move_forward(self):
        return self.board.at(directions.offset(
            self.pivot, self.orientation, self.__class__.length
        )) is None

    def move_forward(self):
        self.pivot = directions.offset(self.pivot, self.orientation)

    def get_actions(self):
        actions = super().get_actions()

        if self.can_move_forward():
            actions.append(Action(self, "move_forward"))

        return actions


# animals can also move backward
class Animal(MoveForwardPiece):
    def can_move_backward(self):
        return self.board.at(directions.offset(
            self.pivot, directions.invert(self.orientation)
        )) is None

    def move_backward(self):
        self.pivot = directions.offset(self.pivot, directions.invert(
            self.orientation)
        )

    def get_actions(self):
        actions = super().get_actions()

        if self.can_move_backward():
            actions.append(Action(self, "move_backward"))

        return actions


class Alligator(Animal):
    length = 3


class Turtle(Animal):
    pass


# boats can rotate
class Boat(MoveForwardPiece):
    def __init__(self, *args, **kwargs):
        self.radiation = 0
        super().__init__(*args, **kwargs)

    def _copy_from(self, original):
        super()._copy_from(original)
        self.radiation = original.radiation

    def radiate(self):
        front_raditaion = self.board.radiation_at(self.front())
        back_radition = self.board.radiation_at(self.pivot)
        self.radiation += max(0, front_raditaion + back_radition)

    def can_rotate(self, clockwise=True):
        offset = Point(0, 1) \
            if self.orientation == "R" or self.orientation == "L" \
            else Point(1, 0)

        # so this may look weird but it is basically saying in a small string
        # out orientation and desired rotation
        # e.g. facing Right and want to rotate clockwise = R>
        rot = self.orientation + (">" if clockwise else "<")

        # now we can check if the point needs to be offset by 1 or -1
        # When rotating basically the points to the side need to get checked
        # this is a simple way to do so by knowing with an orientation and
        # rotation which direction to offset it
        # (yes this could be done in a HUGE if/else but it would look ugly)
        offset *= 1 if \
            rot in ['R>', 'U>', 'L<', 'D<'] \
            else -1  # in ['R<', 'U<', 'L>', 'D>']

        # if the front and back are clear in the direct we can rotate!
        return self.board.at(self.front() + offset) is None \
            and self.board.at(self.pivot + offset) is None

    def rotate_clockwise(self):
        self.orientation = directions.clockwise(self.orientation)

    def rotate_counter_clockwise(self):
        self.orientation = directions.counter_clockwise(self.orientation)

    def get_actions(self):
        actions = super().get_actions()

        if self.can_rotate(True):
            actions.append(Action(self, "rotate_clockwise"))

        if self.can_rotate(False):
            actions.append(Action(self, "rotate_counter_clockwise"))

        return actions
