import os


def read_file(fname='input.txt'):
    fname = os.path.join(
        os.path.dirname(__file__),
        fname
    )
    with open(fname, 'r') as fp:
        return fp.read().strip()


def parse(program):
    """
    Turn program code (str) into list of instructions. 
    Returns a list of tuples. Each tuple represents an instruction
    and is of the form  (<command: str>, <arg: int>)
    """
    parsed = []
    for line in program.strip().split('\n'):
        cmd, arg = line.split(' ')
        arg = int(arg)
        parsed.append((cmd, arg))
    return parsed


def run(program):
    """
    Returns tuple: (<exit_code>, <accumulator_value>)
    Where:
        exit_code=0 when programm reached the end correctly
        exit_code=1 when program was interrupted because an infinite loop occured
    """
    idx = 0
    accumulator = 0
    idx_history = set()
    while idx < len(program) and idx not in idx_history:
        idx_history.add(idx)
        cmd, arg = program[idx]
        if cmd == 'jmp':
            idx += arg
            continue
        elif cmd == 'acc':
            accumulator += arg
        idx += 1
    exit_code = 0 if idx == len(program) else 1
    return exit_code, accumulator


def fix_corruption(program):
    """
    Try swapping jmp/nop operation to find a program that terminates correctly
    """
    corruption_map = {
        'jmp': 'nop',
        'nop': 'jmp',
        'acc': 'acc'  # leave unchanged
    }

    # try fixing each line
    for i, (cmd, arg) in enumerate(program):
        fixed_line = corruption_map[cmd], arg
       
        modified_program = [
            line if i != j 
            else fixed_line
            for j, line in enumerate(program)
        ]
        exit_code, accumulator = run(modified_program)

        if exit_code == 0:
            return accumulator


def test_all():
    test_str = '''nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
'''

    program = parse(test_str)
    exit_code, result = run(program)
    assert result == 5
    assert exit_code == 1


if __name__ == '__main__':
    print('Part 1')
    test_all()
    program = read_file()
    program = parse(program)
    _, result = run(program)
    print(result)

    print('Part 2')
    result = fix_corruption(program)
    print(result)
    