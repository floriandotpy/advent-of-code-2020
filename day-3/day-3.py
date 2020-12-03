import os
from functools import reduce

TREE = '#'
OPEN = '.'


def read_tree_map(fname='input.txt'):
    # always find file, no matter from where this script is called
    fname = os.path.join(
        os.path.dirname(__file__),
        fname
    )

    with open(fname) as fp:
        return [line.replace('\n', '') for line in fp.readlines()]


def coordinates(start_row, start_col, step_row, step_col, last_row):
    while start_row <= last_row:
        yield start_row, start_col
        start_row += step_row
        start_col += step_col


def traverse(tree_map, step_row, step_col):
    # store boundaries of map (note: columns go to infinity, but always repeat)
    num_colums=len(tree_map[0])
    num_rows=len(tree_map)

    # generate coordinates according to step size
    coords = coordinates(
        start_row=step_row,  # skip (0,0)
        start_col=step_col,  # skip (0,0)
        step_row=step_row,
        step_col=step_col,
        last_row=num_rows-1
    )

    # count how many trees we encounter
    count_trees = 0
    for row, col in coords:
        col %= num_colums
        if tree_map[row][col] == TREE:
            count_trees += 1

    return count_trees


if __name__ == "__main__":
    tree_map = read_tree_map()

    print("Part 1")
    result = traverse(
        tree_map,
        step_row=1,
        step_col=3
    )
    print(f"Answer: Encountered {result} trees")

    print("Part 2")
    steps = [
        (1, 1),
        (1, 3),
        (1, 5),
        (1, 7),
        (2, 1) 
    ]
    num_trees = [
        traverse(
            tree_map,
            step_row=step_row,
            step_col=step_col
        ) 
        for step_row, step_col
        in steps
    ]
    product = reduce(lambda a, b: a * b, num_trees)
    print(f"Answer: The product of all trees encountered is {product}")
