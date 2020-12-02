#!/env/python3

"""
Part 1:
From a given list of numbers (`input.txt`), this program finds the two numbers
that sum to 2020 and prints the product of those two numbers.

Part 2: 
From a given list of numbers (`input.txt`), finds the THREE numbers
that sum to 2020 and print their product.
"""

from itertools import product
from timeit import timeit


def read_numbers(fname='input.txt'):
    """
    Read numbers from file `fname` and return as a set of integers.
    """
    with open(fname) as fp:
        numbers = set(int(num) for num in fp.readlines())
    return numbers

# Part 1
def find_pair(numbers, target_sum):
    """
    Find the two numbers that sum to `target_sum` and return their product.
    """
    for num in numbers:
        partner_num = target_sum - num
        if partner_num in numbers:
            return num * partner_num


# Part 2
def find_triplet(numbers, target_sum):
    """
    Find the three numbers that sum to `target_sum` and return their product.
    """
    for num_1, num_2 in product(numbers, numbers):
        partner_num = target_sum - num_2 - num_1

        # leave early if partner would be negative (only tiny speedup, but still)
        if partner_num < 0:
            continue

        if partner_num in numbers:
            return partner_num * num_1 * num_2
                
if __name__ == "__main__":
    target_sum = 2020
    numbers = read_numbers()
    
    num_runs = 1000
    print("Part 1")
    print(find_pair(numbers, target_sum))
    timed = timeit('find_pair(numbers, target_sum)', globals=globals(), number=num_runs)
    print(f'{timed / num_runs * 1_000:.6f} microsec avg')

    print('Part 2')
    print(find_triplet(numbers, target_sum))
    timed = timeit('find_triplet(numbers, target_sum)', globals=globals(), number=num_runs)
    print(f'{timed / num_runs * 1_000:.6f} microsec avg')
