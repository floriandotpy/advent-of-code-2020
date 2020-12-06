#!/usr/bin/env python3

import os
from functools import partial


def read_group_answers(fname='input.txt'):
    # always find file, no matter from where this script is called
    fname = os.path.join(
        os.path.dirname(__file__),
        fname
    )

    with open(fname) as fp:
        groups = [
            group.strip()  # remove leftover whitespace surrounding groups
            for group 
            in fp.read().split('\n\n')  # blank line separates groups
        ]
    return groups


def count_answers(groups, set_fn):
    group_counts = []
    for group in groups:
        answers = [set(answers) for answers in group.split('\n')]
        answers = set_fn(*answers)
        group_counts.append(len(answers))
    return sum(group_counts)


count_unique_answers = partial(count_answers, set_fn=set.union)
count_shared_answers = partial(count_answers, set_fn=set.intersection)


def test_count():
    groups = ['abc', 'a\nb\nc','ab\nac','a\na\na\na', 'b']
    assert count_shared_answers(groups) == 3 + 0 + 1 + 1 + 1
    assert count_unique_answers(groups) == 3 + 3 + 3 + 1 + 1

if __name__ == "__main__":
    test_count()

    group_answers = read_group_answers()

    print('Part 1')
    unique_answers = count_unique_answers(group_answers)
    print(f'In total, the groups gave {unique_answers} unique answers')

    shared_answers = count_shared_answers(group_answers)
    print('Part 2')
    print(shared_answers)
