"""This file is a collection of search algorithms used to find paths for the
boat. New algorithms will be added here, and can be invoked via the CLI.

For the first assignment follow the trace for `bfts()`
"""

import math
_iteration = {'i': 0}


def print_progress(done=False):
    """This just prints progress so we know searches are not frozen

    Args:
        done (Optional[bool]): when True clears the carrier return so print()
            works as expected int he future, and shows the last iteration
    """
    i = _iteration['i']
    _iteration['i'] += 1 if not done else 0
    if done or \
        (i > 1000 and i % 100 == 0) or \
        (i > 500 and i <= 1000 and i % 25 == 0) or \
            i <= 500:
        # slow down the speed at which you print progress as print() statements
        # add time complexity to an already slow process
        print('Searching... {} search iterations'.format(i),
              end='\n' if done else '\r')


# --- Homework 1 algorithms --- #

def bfts(start):
    """Breadth First Tree Search. Basically don't use the came_from graph
    shortcut and make your algorithm super slow. Like so slow you could
    probably fly to China and adopt an orphan and teach them to do it by
    hand faster than this BS.
    """
    return bfs(start, use_came_from=False)


def bfgs(start):
    """Breadth First Graph Search. Basically store if you came from states to
    no re-enqueu them.
    Note: Not part of homework, just my prefered BFS
    """
    return bfs(start, use_came_from=True)


def bfs(start, use_came_from=True):
    """A very basic path finding algorithm (Breadth First Search). When
    given a starting Board, will return a valid path to a Board at a goal state
    Note: because bfts/bfgs are so similar, they are basically combined here,
    where you can choose to record if we have inspected/came_from a board state
    already (bfgs), if disabled this becomes bfts

    Args:
        start (Board): the starting board

    Returns:
        list[Board]: A list of boards representing the path, the the first
            element being a valid child Board to the start, and the
            last element being a Board that is in the goal state.
            If None is returned no possible path exists
    """

    if start.is_boat_at_goal():
        # no need to do anything...
        return []

    # queue of the boards that will have their children searched for goal board
    fringe = []

    # How we got to each board that went into the fringe.
    if use_came_from:
        came_from = {}

    # Enqueue start as the first board to have its children searched.
    fringe.append(start)

    # keep exploring children of children... until there are no more.
    while len(fringe) > 0:
        print_progress()
        # the board we are currently exploring.
        inspect = fringe.pop(0)

        # cycle through the board's children.
        for child in inspect.generate_child_boards():
            # if we found the goal, we have the path!
            if child.is_boat_at_goal():
                # Follow the path backward to the start from the goal and
                #   return it.
                path = [child]

                # Starting at the board we are currently at, insert them
                #   retracing our steps till we get to the starting board
                while inspect != start:
                    path.insert(0, inspect)
                    inspect = inspect.parent_board  # came_from[inspect.str_id]
                return path
            # else we did not find the goal, so enqueue this board's children
            #   to be inspected

            # if the board has not been added to the fringe yet
            if not use_came_from or child.str_id not in came_from:
                # add it to the boards to be explored
                fringe.append(child)
                if use_came_from:
                    came_from[child.str_id] = inspect

    # If we're here, that means that there no path exists to a goal state
    # So signify that by not even giving a path
    return None


# --- Homework 2 Algorithms --- #

def id_dfgs(start):
    """Iterative Deepening Depth First Graph Search
    Basically do Depth First Search, but only up to a given depth. If no path
    id found, increase the given depth by 1 and try again. Keep doing that, and
    if a path exists, we'll find it
    """
    depth = 0
    while True:
        path = dl_dfgs(start, depth, set())
        if path is not None:  # then at this depth we found a path!
            return path
        # else no path was found at this depth, try again at 1 lower
        depth += 1


def dl_dfgs(board, depth, visited):
    """Depth Limited Depth First Graph Search, used in ID-DFGS
    This is a recursive implementation, so the fringe of boards is maintained
    in the call stack, rather than a list() like in BFS above

    I could have edited bfs() above to accommodate dfs via popping off the end
    of the fringe, and adding a depth check, but that is probably just over
    complicating a single function, and this recursive implementation solves
    the puzzles just fine.
    """
    print_progress()

    if board.str_id in visited:
        return  # no need to re-visit node in graph search

    # record this board's hash-able string id as visited so we don't re-visit
    # (graph search)
    visited.add(board.str_id)

    if board.is_boat_at_goal():
        # there is a path to here!
        # recursively reconstruct it using this list
        return []

    if depth > 0:
        for child in board.generate_child_boards():
            path = dl_dfgs(child, depth - 1, visited)
            if path is not None:
                # a path exists, so reconstruct it using this child
                path.insert(0, child)
                return path


# --- Homework 3 Algorithms --- #

def f(n):
    """Used to estimate the cost from board n to the goal
    """
    at_goal = n.at(n.goal.pivot)
    if at_goal is n.boat:
        return 0  # no cost, cause it's a goal state

    # a rough estimate of the distance to the goal from the boat
    d = n.boat.midpoint().manhattan_distance_to(n.goal.pivot)

    # add 1 to the cost because there's something on top of the goal that
    #   needs to be moved, which will require an additional state
    off = 1 if at_goal else 0
    return d + off


def gr_bef_gs(start):
    """Greedy, Best First, Graph Search: Search by using the board that appears
    to be the closest to the goal node using some f(n)
    """

    # boards that we have investigated (graph search)
    visited = set()
    # set of boards open to investigation
    fringe = {str(start): start}

    # scores for boards in one of the sets
    score = {str(start): f(start)}

    while fringe:
        print_progress()

        # find the board in the fringe with the lowest score
        current = None
        for key, board in fringe.items():
            if not current or score[str(board)] < score[str(current)]:
                current = board

        if current.is_boat_at_goal():
            # then we found a path, return it
            path = []
            # reconstruct it
            while current != start:
                path.insert(0, current)
                current = current.parent_board
            return path

        # mark this board as investigated (closed)
        visited.add(str(current))
        fringe.pop(str(current), None)

        # add this boards children to be investigated
        for child in current.generate_child_boards():
            if str(child) not in visited and str(child) not in fringe:
                # calculate the heuristics for child board
                score[str(child)] = f(child)
                # add child board to open set
                fringe[str(child)] = child

    return None  # no path means failure


# --- Homework 4 Algorithms --- #

def h(n):
    """Heuristic, the amount of estimated radiation added to get to the board
    from board n
    """
    steps = f(n)
    rad = min(n.radiation_at(n.boat.pivot), n.radiation_at(n.boat.front()))
    return math.ceil(steps) * (rad + rad)


def g(n):
    return n.boat.radiation


def a_star_gs(start):
    """A pathfinding algorithm (A*) that finds a valid path from this Tile to
    another Tile

    Args:
        start (Board) - the starting board
    Returns:
        (list[Board]) table representing the path. The first element in the
        table will be the first tile in the path, with the last element being
        the goal. An empty table means no path could be found.
    """

    # boards that we have investigated (graph search)
    closed = {}

    # set of boards open to investigation
    fringe = {str(start): start}

    # scores for boards to get from the start to that board
    # The only g_score we know of is the start, which obviously starts at 0
    # as it costs nothing to get to yourself
    g_score = {str(start): 0}

    # for each board, the total cost of getting from the start to the goal
    f_score = {str(start): h(start)}

    while fringe:
        print_progress()

        # find the board in the fringe with the lowest f_score
        current = None
        for key, board in fringe.items():
            if not current or f_score[str(board)] < f_score[str(current)]:
                current = board

        if current.is_boat_at_goal():
            # then we found a path, return it
            path = []
            # reconstruct it
            while current != start:
                path.insert(0, current)
                current = current.parent_board
            return path
        # else: mark this board as investigated (closed)
        closed[str(current)] = True
        del fringe[str(current)]

        # add this boards children to be investigated
        for child in current.generate_child_boards():
            if str(child) in closed:
                continue

            child_g = g(child)

            if str(child) in g_score and child_g >= g_score[str(child)]:
                continue  # as this g_score is higher than the board we know

            fringe[str(child)] = child

            # calculate the heuristics for child board
            g_score[str(child)] = g(child)
            f_score[str(child)] = h(child) + g(child)
