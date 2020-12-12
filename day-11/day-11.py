import os
from copy import deepcopy

EMPTY = 'L'
OCCUPIED = '#'
FLOOR = '.'


def read_file(fname='input.txt'):
    fname = os.path.join(
        os.path.dirname(__file__),
        fname
    )
    with open(fname, 'r') as fp:
        return fp.read().strip()

def parse_input(contents):
    return [list(line) for line in contents.strip().split('\n')]

def print_plan(plan):
    for row in plan:
        print("".join(row))

def plan_coords(height, width):
    return coords(row_from=0, row_to=height-1, col_from=0, col_to=width-1)

def coords(row_from, row_to, col_from, col_to, skip_coords=None):
    for row in range(row_from, row_to+1):
        for col in range(col_from, col_to+1):
            if skip_coords and skip_coords == (row, col):
                continue
            yield row, col

def eight_neighborhood(plan, row, col):
    height, width = len(plan), len(plan[0])
    skip_coords = (row, col)  # ignore self

    # eight_neighborhood is defined as 1 step in each direction, avoid going over map boundaries
    row_from = max(row - 1, 0)
    col_from = max(col - 1, 0)
    row_to = min(row + 1, height - 1)
    col_to = min(col + 1, width - 1)

    return [
        plan[row][col]
        for row, col 
        in coords(row_from, row_to, col_from, col_to, skip_coords=skip_coords)
    ]

def ray_coords(row_start, row_stop, col_start, col_stop, row_step, col_step):
    num_rows = (abs(row_stop - row_start) + 1)
    num_cols = (abs(col_stop - col_start) + 1)
    
    if row_step == 0:
        rows = [row_start] * num_cols
    else:
        rows = range(row_start, row_stop+row_step, row_step)
    
    if col_step == 0:
        cols = [col_start] * num_rows
    else:
        cols = range(col_start, col_stop+col_step, col_step)

    return zip(rows, cols)
    

def ray(plan, row, col, row_step, col_step, look_for, skip_first=True):
    """
    Traverse a line across `plan` starting from location `row`, `col`
    and goind in direction `row_step`, `col_step` until one of the values
    in `look_for` is found. 
    Returns:
     - the value that was found (one of the values from `look_for`.
     - None, if nothing is found once the edge of the plan is reached
    """
    height, width = len(plan), len(plan[0])

    # boundaries in direction of day (index is inclusive)
    row_stop = 0 if row_step < 0 else height - 1
    col_stop = 0 if col_step < 0 else width - 1
    ray = ray_coords(row, row_stop, col, col_stop, row_step, col_step)
    if skip_first:
        next(ray)
    for r, c in ray:
        seat = plan[r][c]
        if seat in look_for:
            return seat
    
    # nothing found
    return None


def visible_neighborhood(plan, row, col):
    look_for = (EMPTY, OCCUPIED)
    seats = [
        ray(plan, row, col, row_step, col_step, look_for)
        for (row_step, col_step) in
        [
            (-1, -1),  # up left
            (-1, 0),  # up
            (-1, 1),  # up right
            (0, -1),  # left
            (0, 1), # right
            (1, -1), # down left
            (1, 0), # down
            (1, 1)  # down right
        ]
    ]

    # Remove None
    return list(filter(bool, seats))


def step(plan: list, neighborhood_fn, empty_threshold):
    height, width = len(plan), len(plan[0])
    plan_after = deepcopy(plan)

    changed = False
    for row, col in plan_coords(height, width):
        neighbors = neighborhood_fn(plan, row, col)
        occupied_neighbors = [n for n in neighbors if n == OCCUPIED]
        seat = plan[row][col]
        if seat == EMPTY and not occupied_neighbors:
            # If a seat is empty (L) and there are no occupied seats
            # adjacent to it, the seat becomes occupied.
            seat = OCCUPIED
            changed = True
        elif seat == OCCUPIED and len(occupied_neighbors) >= empty_threshold:
            # If a seat is occupied (#) and four or more seats adjacent
            # to it are also occupied, the seat becomes empty.
            seat = EMPTY
            changed = True
        # Otherwise, the seat's state does not change.

        plan_after[row][col] = seat

    return plan_after, changed

def step_until_convergence(plan, neighborhood_fn, empty_threshold=4, log=True):
    changed = True
    while changed:
        if log:
            print(f'------')
            print_plan(plan)
        plan, changed = step(plan, neighborhood_fn, empty_threshold)
    
    return sum([len(list(filter(lambda seat: seat == OCCUPIED, row))) for row in plan])


def test_plan_coords():
    coords = plan_coords(height=4, width=5)
    assert len(list(coords)) == 4 * 5


def test_ray_coords():

    # main diagonal
    actual = ray_coords(row_start=0, row_stop=3, col_start=0, col_stop=3, row_step=1, col_step=1)
    actual = list(actual)
    print(actual)
    assert actual == [(0, 0), (1, 1), (2, 2), (3, 3)]

    # diagonal reverse
    actual = ray_coords(row_start=4, row_stop=0, col_start=3, col_stop=0, row_step=-1, col_step=-1)
    actual = list(actual)
    print(actual)
    assert actual == [(4, 3), (3, 2), (2, 1), (1, 0)]

    # straight up
    actual = ray_coords(row_start=4, row_stop=0, col_start=3, col_stop=0, row_step=-1, col_step=0)
    actual = list(actual)
    print(actual)
    assert actual == [(4, 3), (3, 3), (2, 3), (1, 3), (0, 3)]


def test_eight_neighborhood():
    test_plan = ['...', '.X.', '...']
    actual = eight_neighborhood(test_plan, row=1, col=1)
    assert actual == ['.' for _ in range(8)]

    # top left corner should have 3 neighbors
    actual = eight_neighborhood(test_plan, row=0, col=0)
    assert actual == list('..X')

    # top right corner should have 3 neighbors
    actual = eight_neighborhood(test_plan, row=0, col=2)
    assert actual == list('.X.')


def test_visible_neighborhood():
    plan_eight = parse_input(""".......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....""")
    row, col = 4, 3  # empty seat as start point
    assert plan_eight[row][col] == EMPTY
    actual = visible_neighborhood(plan_eight, row, col)
    print(actual)
    assert actual == [OCCUPIED for _ in range(8)]

    # from start seat, only empty floor is visble
    plan_zero = parse_input(""".##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.""")
    row, col = 3, 3
    assert plan_zero[row][col] == EMPTY
    actual = visible_neighborhood(plan_zero, row, col)
    assert actual == []

    # only 1 empty seat is visible, others are hidden
    plan_one_empty = parse_input(""".............
.L.L.#.#.#.#.
.............""")
    row, col = 1, 1
    assert plan_one_empty[row][col] == EMPTY
    actual = visible_neighborhood(plan_one_empty, row, col)
    assert actual == [EMPTY]


def test_all():
    test_plan_coords()
    test_eight_neighborhood()
    test_ray_coords()
    test_visible_neighborhood()

    test_str = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

    plan = parse_input(test_str)
    num_seats = step_until_convergence(plan, neighborhood_fn=eight_neighborhood, log=False)
    assert num_seats == 37

if __name__ == "__main__":
    test_all()

    contents = read_file()
    plan = parse_input(contents)
    
    print('Part 1')
    num_seats = step_until_convergence(plan, neighborhood_fn=eight_neighborhood, log=False)
    # Q: How many seats end up occupied?
    print(num_seats)

    print('Part 2')
    num_seats = step_until_convergence(plan, neighborhood_fn=visible_neighborhood, empty_threshold=5, log=False)
    print(num_seats)
