#!/usr/bin/env python3

import os


def binary_str_to_int(value, high='1', low='0'):
    value = value.replace(high, '1').replace(low, '0')
    return int(value, 2)


def parse_boarding_pass(value):
    row = binary_str_to_int(value[:7], high='B', low='F')
    col = binary_str_to_int(value[7:10], high='R', low='L')
    seat = 8 * row + col
    return seat


def test_parse_boarding_pass():
    assert parse_boarding_pass('BFFFBBFRRR') == 567
    assert parse_boarding_pass('FFFBBBFRRR') == 119
    assert parse_boarding_pass('BBFFBBFRLL') == 820.


def read_boarding_plan(fname='input.txt'):
    """
    Read boarding plan from text file.
    Returns a list of integers.
    Each integer is a seat id on the plane.
    """

    # always find file, no matter from where this script is called
    fname = os.path.join(
        os.path.dirname(__file__),
        fname
    )

    with open(fname) as fp:
        boarding_passes = [
            parse_boarding_pass(boarding_pass)
            for boarding_pass
            in fp.readlines()
        ]

    return boarding_passes


if __name__ == "__main__":
    test_parse_boarding_pass()
    seat_ids = read_boarding_plan()
    print('Part 1')
    print(f'Largest seat id: {max(seat_ids)}')

    print('Part 2')
    seat_ids = sorted(seat_ids)
    for seat_a, seat_b in zip(seat_ids[:-1], seat_ids[1:]):
        if seat_b - seat_a == 2:
            print(f'Free seat: {seat_b - 1}')
    