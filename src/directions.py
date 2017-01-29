"""This is a collection of helper functions to deal with directions

All assume a valid "direction" is 'U', 'R', 'D' or 'L'
"""

from point import Point


def clockwise(direction):
    """Rotates a direction clockwise, e.g. 'U' -> 'R'

    Args:
        direction (str): a valid direction ('U', 'R', 'D' or 'L')

    Returns:
        str: the direction rotated clockwise
    """
    if direction == "U":
        return "R"
    if direction == "R":
        return "D"
    if direction == "D":
        return "L"
    return "U"


def invert(direction):
    """Inverts a direction to the opposite direction, e.g. 'U' -> 'D'

    Args:
        direction (str): a valid direction ('U', 'R', 'D' or 'L')

    Returns:
        str: the direction inverted to the opposite direction
    """
    if direction == "U":
        return "D"
    if direction == "D":
        return "U"
    if direction == "R":
        return "L"
    return "R"


def counter_clockwise(direction):
    """Rotates a direction counterclockwise, e.g. 'U' -> 'R'

    Args:
        direction (str): a valid direction ('U', 'R', 'D' or 'L')

    Returns:
        str: the direction rotated counterclockwise
    """
    if direction == "U":
        return "L"
    if direction == "L":
        return "D"
    if direction == "D":
        return "R"
    return "R"


def offset(point, direction, distance=1):
    """Offsets a point in a given direction some distance,
    E.g. (0, 0) offset 'R' by 2 => (2, 0)

    Args:
        point (Point): the point to use for the offset point
        direction (str): a valid direction ('U', 'R', 'D' or 'L')
        distance (Optional[int]): the distance to offset, defaults to 1

    Returns:
        Point: a new point, offset from the passed in point in the direction
    """
    if direction == "U":
        return Point(point.x, point.y - distance)
    if direction == "R":
        return Point(point.x + distance, point.y)
    if direction == "D":
        return Point(point.x, point.y + distance)
    if direction == "L":
        return Point(point.x - distance, point.y)
    return point
