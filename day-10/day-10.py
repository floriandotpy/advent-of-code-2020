import os
from collections import Counter
from functools import reduce


def read_file(fname='input.txt'):
    fname = os.path.join(
        os.path.dirname(__file__),
        fname
    )
    with open(fname, 'r') as fp:
        return fp.read().strip()


def parse_input(content: str):
    return [int(num) for num in content.strip().split('\n')]


def find_adapter_chain_diffs(
    adapters: list,
    outlet=0,
    adapter_tolerance=-3,
    device_tolerance=+3):

    diffs = Counter()
    
    # sort adapters by their output joltage
    adapters.sort()

    # add own device as it acts as final adapter 
    adapters.append(adapters[-1] + device_tolerance)

    for jolt_in, jolt_out in zip([outlet] + adapters[:-1], adapters):
        diff = jolt_out - jolt_in
        # print(f'{jolt_in} -> {jolt_out}, {diff}')
        diffs[diff] += 1

    return diffs


def count_chain_combinations(
    adapters: list,
    outlet=0,
    adapter_tolerance=abs(-3),
    device_tolerance=+3):

    # Add own device as it acts as final adapter 
    adapters.append(max(adapters) + device_tolerance)
    
    # Add outlet as it acts like a fixed adapter
    adapters.append(outlet)

    # Sort adapters by their output joltage so that we can iterate in order
    adapters.sort()

    # Map from each adapter to compatible adapters than can be plugged into the first one
    adapter_partners = {}
    for idx, adapter in enumerate(adapters):
        compatible = {p for p in adapters[idx+1:] if p <= adapter + adapter_tolerance}
        adapter_partners[adapter] = compatible
    
    # Iteratively count how many adapter paths to the device exist
    num_combinations = {}
    for adapter in reversed(adapters):  # reversed, as we start at the device
        compatible = adapter_partners[adapter]
        if not compatible:  # end of the chain (=the device)
            num_combinations[adapter] = 1 
        else: 
            num_combinations[adapter] = sum(num_combinations[p] for p in compatible)

    return num_combinations[adapters[0]]


def test_all():
    test_str_1 = """16
10
15
5
1
11
7
19
6
12
4"""


    test_str_2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

    adapters = parse_input(test_str_1)
    diffs = find_adapter_chain_diffs(adapters)
    assert diffs[1] == 7
    assert diffs[3] == 5

    num_combinations = count_chain_combinations(adapters)
    assert num_combinations == 8

    adapters_2 = parse_input(test_str_2)
    num_combinations_2 = count_chain_combinations(adapters_2)
    assert num_combinations_2 == 19208


if __name__ == "__main__":
    test_all()

    contents = read_file()
    adapters = parse_input(contents)
    diffs = find_adapter_chain_diffs(adapters)
    print('Part 1')
    # Q: What is the number of 1-jolt differences multiplied by the number of
    #    3-jolt differences?
    print(diffs[1] * diffs[3])

    print('Part 2')
    # Q: What is the total number of distinct ways you can arrange the adapters
    #    to connect the charging outlet to your device?
    print(count_chain_combinations(adapters))
