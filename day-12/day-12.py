import os

# Action N means to move north by the given value.
# Action S means to move south by the given value.
# Action E means to move east by the given value.
# Action W means to move west by the given value.
# Action L means to turn left the given number of degrees.
# Action R means to turn right the given number of degrees.
# Action F means to move forward by the given value in the direction the ship is currently facing.
NORTH = 'N'
SOUTH = 'S'
EAST = 'E'
WEST = 'W'
LEFT = 'L'
RIGHT = 'R'
FORWARD = 'F'
MOVES = (NORTH, SOUTH, EAST, WEST)
TURNS = (LEFT, RIGHT)

DIRECTION_TO_VECTOR = {
    EAST: (0, 1),
    SOUTH: (1, 0),
    WEST: (0, -1),
    NORTH: (-1, 0)
}

# map orienation angle to movement vector
ANGLE_TO_VECTOR = {
    0: DIRECTION_TO_VECTOR[EAST],
    90: DIRECTION_TO_VECTOR[SOUTH],
    180: DIRECTION_TO_VECTOR[WEST],
    270: DIRECTION_TO_VECTOR[NORTH]
}

def read_file(fname='input.txt'):
    fname = os.path.join(os.path.dirname(__file__), fname)
    with open(fname, 'r') as fp:
        return fp.read().strip()


def parse_input(contents):
    return [
        (line[:1], int(line[1:]))
        for line in 
        contents.strip().split('\n')
    ]

def rotate_90deg(point):
    """
    Rotate by 90 degrees clockwise using a little trick to avoid matrix math
    https://limnu.com/sketch-easy-90-degree-rotate-vectors/
    """
    row, col = point
    return col, -row


def run(actions, start_position, waypoint=None):
    # Ship position; tuple indicating (north, east)
    position = start_position
    # Ship rotation. If `waypoint` is set, ship rotation is not used
    rotation = 0  # facing east by default
    
    # Step through all actions
    for action, value in actions:

        # Read motion and rotation parameters from action
        if action in MOVES:
            vec = DIRECTION_TO_VECTOR[action]
            d_position = vec[0] * value, vec[1] * value
            d_rotation = 0
        elif action == RIGHT:
            d_position = (0, 0)
            d_rotation = value
        elif action == LEFT:
            d_position = (0, 0)
            d_rotation = -1 * value
        elif action == FORWARD:
            vec = ANGLE_TO_VECTOR[rotation]
            d_position = vec[0] * value, vec[1] * value
            d_rotation = 0
        else:
            raise RuntimeError(f'unsupported action: {action}')

        # EVALUATION: Modify waypoint (if set), and/or ship position
        if waypoint and action == FORWARD:
            # move ship according to waypoint (=movement vector)
            position = (
                position[0] + waypoint[0] * value, 
                position[1] + waypoint[1] * value
            )

        elif waypoint and action in MOVES:
            # move waypoint itself
            waypoint = (waypoint[0] + d_position[0], waypoint[1] + d_position[1])

        elif waypoint and action in TURNS:
            # force angle to positiv range
            while d_rotation < 0:
                d_rotation += 360
            # split into multiples of 90 degrees
            num_rotations = d_rotation//90
            # rotate n times by 90 degrees
            for _ in range(num_rotations):
                waypoint = rotate_90deg(waypoint)
    
        else:
            # no waypoint? All actions affect ship position directly
            position = (position[0] + d_position[0], position[1] + d_position[1])
            rotation = (rotation + d_rotation) % 360

    return position


def dist(pos_a, pos_b):
    """
    Compute Manhattan distance between two points
    Manhatten distance is the sum of the absolute values of
    its east/west position and its north/south position
    """
    return sum([abs(a - b) for a, b in zip(pos_a, pos_b)])


def test_all():
    test_contents = """F10
N3
F7
R90
F11"""

    actions = parse_input(test_contents)
    start_position = (0, 0)
    end_position = run(actions, start_position)
    result = dist(start_position, end_position)
    assert result == 25

    end_position = run(actions, start_position, waypoint=(-1, 10))
    result = dist(start_position, end_position)
    # After these operations, the ship's Manhattan distance from its starting position is 214 + 72 = 286.
    assert result == 286


def main():
    actions = read_file()
    actions = parse_input(actions)

    print('Part 1')
    # Q: What is the Manhattan distance between the final postion and the ship's starting position?
    start_position = (0, 0)
    end_position = run(actions, start_position)
    result = dist(start_position, end_position)
    print(result)

    # Q: What is the Manhattan distance between the final postion and the ship's starting position?
    print('Part 2')
    start_position = (0, 0)
    end_position = run(actions, start_position, waypoint=(-1, 10))
    result = dist(start_position, end_position)
    print(result)

if __name__ == "__main__":
    test_all()
    main()
