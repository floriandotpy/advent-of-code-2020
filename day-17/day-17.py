"""
Implementation notes:

To represent the "infinite" grid with negative and positive
coordinates, I chose a plain Python dictionary with tuples
as the keys. Each tuple is one coordinate.

The downside is that in contrast to n-dimensional lists 
(or numpy arrays), it is non-trivial to iterate through the
grid in order. However, this was not needed for the solution.
As the index lookup of a dictionary is fast, there is also no
real drag on performance for these smaall structures.

One downside is that I am traversing some points multiple times
when I check the neighborhood, but as this also happens through
an index lookup, I think it's fine. For a large point cloud you
would obviously make this a little smarter and omptimized.
"""

from itertools import product


ACTIVE = '#'
INACTIVE = '.'


def neigborhood_3d(x, y, z, include_center=True):

    for x_, y_, z_ in product(
        range(x-1, x+2),  # +2 because `stop` param is exclusive
        range(y-1, y+2),
        range(z-1, z+2)
    ):
        if include_center or (x_, y_, z_) != (x, y, z):
            yield x_, y_, z_


def neigborhood_4d(x, y, z, w, include_center=True):

    for x_, y_, z_, w_ in product(
        range(x-1, x+2),  # +2 because `stop` param is exclusive
        range(y-1, y+2),
        range(z-1, z+2),
        range(w-1, w+2)
    ):
        if include_center or (x_, y_, z_, w_) != (x, y, z, w):
            yield x_, y_, z_, w_


def parse_input(contents, dims=3):
    lines = contents.strip().split('\n')
    
    # map from tuple coordinates to value at that location
    grid = {}
    z = 0
    w = 0  # only used if dims==4
    for y, line in enumerate(lines):
        for x, value in enumerate(line):
            coords = (x, y, z)
            if dims == 4:  # append 4th dimension
                coords += (w,)
            grid[coords] = value
    
    return grid


def count_active(grid, points):
    values = [grid.get(loc) for loc in points]
    values = [v for v in values if v == ACTIVE]
    return len(values)


def step(before, neigborhood=None):
    neigborhood = neigborhood or neigborhood_3d
    after = {}

    # collect all points to consider, even the ones currently not covered by grid
    coords_to_consider = set()
    for point in before.keys():
        for neighbor in neigborhood(*point):
            coords_to_consider.add(neighbor)
    
    for loc in coords_to_consider:
        loc_is_active = (before.get(loc) == ACTIVE)
        num_active_neighbors = count_active(before, neigborhood(*loc, include_center=False))
        if loc_is_active:
            if num_active_neighbors in (2, 3):
                # If a cube is active and exactly 2 or 3 of its neighbors 
                # are also active, the cube remains active.
                after[loc] = ACTIVE
            else:
                # Otherwise, the cube becomes inactive.
                # after[loc] = INACTIVE
                pass
        else:
            if num_active_neighbors == 3:
                # If a cube is inactive but exactly 3 of its neighbors 
                # are active, the cube becomes active. 
                after[loc] = ACTIVE
            else:
                # Otherwise, the cube remains inactive.
                # after[loc] = INACTIVE
                pass
            
    return after


def test():

    assert len(list(neigborhood_3d(0,0,0))) == 27, len(list(neigborhood_3d(0,0,0)))
    assert len(list(neigborhood_3d(0,0,0, include_center=False))) == 26

    s = """.#.
..#
###"""

    grid_3d = parse_input(s)
    assert len(grid_3d.keys()) == 3*3
    assert all(val in (ACTIVE, INACTIVE) for val in grid_3d.values())

    for _ in range(6):
        grid_3d = step(grid_3d)
        
    num_active = count_active(grid_3d, grid_3d.keys())
    assert num_active == 112, num_active

    grid_4d = parse_input(s, dims=4)
    assert all(len(k) == 4 for k in grid_4d.keys())
    for _ in range(6):
        grid_4d = step(grid_4d, neigborhood=neigborhood_4d)
        
    num_active = count_active(grid_4d, grid_4d.keys())
    assert num_active == 848, num_active


def main():
    # Actual input
    s = """.#.##..#
....#.##
##.###..
.#.#.###
#.#.....
.#..###.
.#####.#
#..####."""


    print('Part 1')
    grid_3d = parse_input(s)
    for _ in range(6):
        grid_3d = step(grid_3d)
    num_active = count_active(grid_3d, grid_3d.keys())
    print(num_active)

    print('Part 2')
    grid_4d = parse_input(s, dims=4)
    for _ in range(6):
        grid_4d = step(grid_4d, neigborhood=neigborhood_4d)
    num_active = count_active(grid_4d, grid_4d.keys())
    print(num_active)


if __name__ == "__main__":
    test()
    main()
