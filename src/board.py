from pieces import Piece, Alligator, Turtle, Tree, Boat, Goal

# used to print things to console all pretty like
_str_mapping = {
    None.__class__: " .",
    Alligator: "A#",
    Turtle: "T#",
    Tree: "C#",  # because they are Cyprus Trees or whatever
    Boat: "B@",  # will be replaced with an arrow
    Goal: " G"
}

# used to represent a direction by an arrow, cause it's easier to understand
_str_arrow = {
    'U': '^',
    'R': '>',
    'D': 'V',
    'L': '<',
}


class Board():
    """Holds Pieces and represents a game state
    """
    _id = 0

    def __init__(self, action=None):
        """Creates a new board. Passing an action assumes this is a Board state
        derived from the the initial state

        Args:
            action (Optional[Action]): the action that this state is derived
            from
        """
        self._id = Board._id
        Board._id += 1
        self.width = None
        self.height = None

        self.radiation_source = None
        self.radition_magnitude = None
        self.radition_decay = None

        self.alligators = None
        self.turtles = None
        self.trees = None

        self.boat = None

        self.goal = None

        if action:
            self._apply_action(action)

    def _apply_action(self, action):
        """Applies an action, this deriving this board from it (cloning it and
        updating based on action)

        Args:
            action (Action): The action to apply and clone from
        """
        self._clone_from(action.board)

        self.parent_board = action.board
        self.parent_action = action

        if action.piece_name == "Boat":
            piece = self.boat
        else:
            pieces = self.alligators \
                if action.piece_name == "Alligator" else self.turtles
            piece = pieces[action.piece_index]

        # invoke the method of that piece via reflection
        getattr(piece, action.method)()

        if not self.is_boat_at_goal():
            self.boat.radiate()

        self.update()

    def _clone_from(self, original):
        """Clones all internal [public] members from an original board to this

        Args:
            original (Board): the original board that we need to copy all data
            from. Note: new Piece instances are created instead of justing
            creating a shallow copied
        """
        for member in dir(original):
            if callable(getattr(original, member)) or member.startswith("_"):
                continue

            val = getattr(original, member)
            clone = val

            if isinstance(val, list):
                clone = [item.clone(board=self) for item in val]
            elif isinstance(val, Piece):
                clone = val.clone(board=self)
            # else it's some primitive like a number

            # set that member to us via reflection
            setattr(self, member, clone)

    def _parse(self, contents):
        """Parsed the contents of a file to a board state

        Yes the file format is stupid, whatever

        Args:
            contents (string): the contents of a puzzle file.
                Must be in the correct format
        """
        for line in contents.splitlines():
            split = line.split()
            # each line will always be 3 things, two numbers,
            #   followed by an optional letter
            first = int(split[0])
            second = int(split[1])
            third = split[2] if len(split) == 3 else None

            if self.width is None:
                # then this is the 1st line, so record the width/height
                self.width = first
                self.height = second
            elif self.radiation_source is None:
                # 2nd line, so record the rad source
                self.radiation_source = Point(first, second)
            elif self.radition_magnitude is None:
                # 3rd line, which is rad mag followed by decay
                self.radition_magnitude = first
                self.radition_decay = second
            elif self.alligators is None:
                # 4th line, which is the number of alligators, turtles, & trees
                self.alligators = [None] * first
                self.turtles = [None] * second
                # `third` is actually an integer here (number of trees)
                self.trees = [None] * int(third)
            elif None in self.alligators:
                # we are recoding alligators
                index = self.alligators.index(None)
                self.alligators[index] = Alligator(
                    board=self,
                    index=index,
                    x=first,
                    y=second,
                    orientation=third
                )
            elif None in self.turtles:
                # we are recording turtles
                index = self.turtles.index(None)
                self.turtles[index] = Turtle(
                    board=self,
                    index=index,
                    x=first,
                    y=second,
                    orientation=third
                )
            elif None in self.trees:
                # we are recoding trees
                index = self.trees.index(None)
                self.trees[index] = Tree(
                    board=self,
                    index=index,
                    x=first,
                    y=second
                )
            elif self.boat is None:
                # second to last line, the boat
                self.boat = Boat(
                    board=self,
                    x=first,
                    y=second,
                    orientation=third
                )
            elif self.goal is None:
                # last line, the goal point
                self.goal = Goal(
                    board=self,
                    x=first,
                    y=second
                )
            # else: shouldn't happen, or blank line(s) at the end of the file

    def update(self):
        """Called or needs to be called after something internally changes.
        Should be called after being filled from the file formatter or from
        within after cloning Pieces
        """

        # store all the "things" on the board in one handy list
        self._pieces = [self.boat, self.goal] + self.alligators + \
            self.turtles + self.trees

        self._grid = []
        for x in range(self.width):
            self._grid.append([])
            for y in range(self.height):
                self._grid[x].append(None)

                for obj in self._pieces:
                    if obj.at(x, y) and obj is not self.goal:
                        self._grid[x][y] = obj
                        break

        self._generate_str_id()

    def at(self, x, y=None):
        """Determine what (if anything) is at passed in coordinate or Point

        Args:
            x (int, Point): the x coordinate, or the actual Point instance
            y (Optional[int]): the y coordinate if x was not the Point

        Returns:
            None, Piece, str: If nothing is at the (x, y) None is returned,
            if the given (x, y) was out of bounds, the string "Out of Bounds"
            is returned. Otherwise if a Piece was present that Piece is
            returned
        """
        if y is None:
            # x is a point
            y = x.y
            x = x.x
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return "Out of Bounds"
        return self._grid[x][y]

    def radiation_at(self, point):
        """Gets the amount of radiation present at a given point on the grid

        Args:
            point (Point): the point in the grid to check, must lie within the
            width/height of the board

        Returns:
            int: an integer >= 0 representing how much radiation that will be
            incurred at the given point
        """
        d = self.radiation_source.manhattan_distance_to(point)
        return max(0, self.radition_magnitude - (d*self.radition_decay))

    def get_valid_actions(self):
        """Gets a list of all valid Actions that this Board state can perform

        Returns:
            list[Action]: the list of all valid actions that this Board state
            can perform (none will have been applied to anything upon being
            returned from this function however)
        """
        valid_actions = []
        for piece in self._pieces:
            valid_actions.extend(piece.get_actions())

        return valid_actions

    def generate_child_boards(self):
        """Use all the valid Actions that this Board state can do to generate
        the child Boards and return them in a list

        Returns:
            list[Board]: All new Boards that have applied the possible Actions
            of this board, and thus are children of this Board. Use this to
            build the state tree
        """
        return [
            action.generate() for action in self.get_valid_actions()
        ]

    def is_boat_at_goal(self):
        """Checks if at this Board state the Boat is at the Goal point

        Returns:
            bool: True if this is a goal state, False otherwise
        """
        return self.boat.at(self.goal.pivot)

    def _generate_str_id(self):
        """Generates a nifty ASCII art representation of the Board, that is also
        unique (except for radiation) to be used as a quick ID for comparisons

        Returns:
            str: a string (with newlines) that shows what the Board looks like
        """
        lines = []
        for y in range(self.height):
            line = []
            for x in range(self.width):
                obj = self.at(x, y)
                rep = _str_mapping[obj.__class__]
                if obj is not None:
                    rep = rep.replace('#', str(obj.index))
                elif self.goal.at(x, y):
                    rep = " G"

                if isinstance(obj, Boat):
                    # show the direction
                    if obj.pivot.x == x and obj.pivot.y == y:
                        rep = rep.replace(
                            '@',
                            '-' if obj.orientation in ['L', 'R'] else '|'
                        )
                    else:
                        rep = rep.replace("@", _str_arrow[obj.orientation])

                if isinstance(obj, Boat):
                    # direction
                    pass

                # pad with 1 space so it looks better
                line.append(rep)
            lines.append(" ".join(line))  # pad with a space for pretty-ness
        self.str_id = "\n".join(lines)

    def __repr__(self):
        """string representation override

        Returns:
            str: the string id (which is also ASCII art)
        """
        return self.str_id
