import os

def read_file(fname='input.txt'):
    fname = os.path.join(
        os.path.dirname(__file__),
        fname
    )
    with open(fname, 'r') as fp:
        return fp.read().strip()


def parse(contents):
    return [int(num) for num in contents.strip().split('\n')]


def find_pair(numbers, target_sum):
    """
    Find the two numbers that sum to `target_sum` and return them as a tuple.
    Returns None if no pair sums to the target_sum.
    """
    for num in numbers:
        partner_num = target_sum - num
        if partner_num in numbers:
            return num * partner_num
    return None


def find_invalid_number(numbers, n=25):
    """
    Check all numbers for being "valid". 
    A "valid" number is a number that can be represented
    by the sum of any two numbers from its preceding `n` numbers.
    Vice versa, an invalid number is a number that does not
    fulfil this criterion.

    Returns the first invalid number that's found in the list
    or None if no invalid number is found.
    """
    for i, num in enumerate(numbers[n:]):
        prev = set(numbers[i:n+i])
        if not find_pair(prev, target_sum=num):
            return num
    return None


def find_cont_sequence(numbers, target_sum):
    """
    Find a continuous sequence if numbers in `numbers` that sum to `target_sum`.
    Returns the smallest and largest number of that sequence (as a tuple).
    Returns None if no sequence found.
    """

    for seq_len in range(2, len(numbers)):
        for start in range(len(numbers) - seq_len):
            seq = numbers[start:start+seq_len]
            if sum(seq) == target_sum:
                return min(seq), max(seq)


def test_all():
    test_input = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""

    numbers = parse(test_input)
    num = find_invalid_number(numbers, n=5)
    assert num == 127

    a, b = find_cont_sequence(numbers, num)
    assert (a, b) == (15, 47)
    assert a + b == 62

if __name__ == "__main__":
    test_all()

    contents = read_file()
    numbers = parse(contents)
    
    print('Part 1')
    result = find_invalid_number(numbers)
    print(result)

    print('Part 2')
    a, b = find_cont_sequence(numbers, target_sum=result)
    print(a + b)
