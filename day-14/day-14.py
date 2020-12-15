import re
import os


regex_mem = re.compile(r'mem\[(\d+)\] = (\d+)')


def read_file(fname='input.txt'):
    fname = os.path.join(os.path.dirname(__file__), fname)
    with open(fname, 'r') as fp:
        return fp.read().strip()


def parse_mask(mask):
    return {
        idx: int(bit) for idx, bit in enumerate(reversed(mask)) if bit != 'X'
    }


def parse_input(s):
    print('ok')
    output = []
    for line in s.strip().split('\n'):
        line = line.strip()
        if line.startswith('mask'):
            mask = parse_mask(line.split(' = ')[1])
            # print('and_mask', and_mask)
            # print('or_mask ', or_mask)
            args = mask
            output.append(
                ('mask', args)
            )
        elif line.startswith('mem'):
            # mem[7] = 101
            m = regex_mem.match(line)
            addr = int(m.group(1))
            value = int(m.group(2))
            args = addr, value
            output.append(('mem', args))
        else:
            raise ValueError(f'Unknown command in line: {line}')

    return output


def apply(mask, value):
    for idx, bit in mask.items():
        if bit is 0:
            # clear bit
            value = value & ~(1 << idx)
        elif bit is 1:
            # set bit
            value = value | (1 << idx)
    return value


def run(program):
    mem = {}
    mask = {}
    for cmd, args in program:
        if cmd == 'mask':
            mask = args
        elif cmd == 'mem':
            addr, value = args
            value = apply(mask, value)
            mem[addr] = value

    # What is the sum of all values left in memory after it completes?
    return sum(mem.values())


def test_apply():
    mask = {0: 0}  # force LSB to zero
    value = 1  # 0001
    expected = 0 # 0000
    actual = apply(mask, value)
    assert expected == actual, actual
    
    value = 7  # 0111
    expected = 5  # 0101
    mask = {1: 0}
    actual = apply(mask, value)
    assert expected == actual, actual

    mask = {1: 1}
    value = 5  # 0101
    expected = 7  # 0111
    actual = apply(mask, value)
    assert expected == actual, actual


    actual = apply(mask, value)
    assert expected == actual, actual
    

def test_parse_mask():

    assert parse_mask('X1X') == {1: 1}
    assert parse_mask('XX0') == {0: 0}
    assert parse_mask('01X') == {1: 1, 2: 0}


def test_all():
    test_apply()
    test_parse_mask()

    s = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

    program = parse_input(s)
    result = run(program)
    assert result == 165


def main():
    s = read_file()
    program = parse_input(s)

    print('Part 1')
    result = run(program)
    print(result)


if __name__ == '__main__':
    test_all()
    main()
