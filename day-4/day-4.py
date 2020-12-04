#!/usr/bin/env python3

"""
Solution for Day 4: Load and parse a text file of "passports".
Each passports has a number of fields with values, encoded as pairs:

eyr:2020 ecl:blu hcl:#cfa07d pid:097863725
hgt:150cm
byr:1951
cid:143 iyr:2013

This script validates:
1. That all required fields are present for a passport. 
   To get the answer for part 1, we count how many passports are "valid"
2. That all required fields also validate according to
   a number of rules (for example: valid year of birth). The answer
   to part 2 is also the number of passports which fulfill this second
   validation check.

Implementation notes:
  - Regular expressions for parsing and validation
  - list and dict comprehensions wherever it made sense
  - Useing `functools.partial` to bind parameter values to a wrapped function
  - Using Python `assert` statements for test cases, in order to check that
    the validation rules are implemented correctly
"""

import os
import re
from functools import partial

regex_year = re.compile(r'^\d{4}$')
regex_height = re.compile(r'(\d+)(in|cm)')
regex_color = re.compile(r'^\#(\d|[abcdef]){6}$')

required_fields = [
    'byr',  # Birth Year
    'iyr',  # Issue Year
    'eyr',  # Expiration Year
    'hgt',  # Height
    'hcl',  # Hair Color
    'ecl',  # Eye Color
    'pid',  # Passport ID
]


###############################
# Passport loading and parsing
###############################

def parse_passport_str(passport_str):
    """
    Turn a passport string representation into a dictionary.
    """
    pairs = [pair.split(':') for pair in passport_str.split(' ')]
    return {
        k: v 
        for k, v 
        in pairs
    }

def read_passport_db(fname='input.txt'):
    """
    Read passport db from text file.
    Returns a list of dictionaries where each dictionary represents a single passport.
    """

    # always find file, no matter from where this script is called
    fname = os.path.join(
        os.path.dirname(__file__),
        fname
    )

    with open(fname) as fp:
        passports = [
            passport
            .replace('\n', ' ')  # remove any line breaks 
            .strip()  # remove all leading/trailing whitespace
            for passport
            in fp.read().split('\n\n')  # blank line separates entries
        ]

    return [parse_passport_str(passport) for passport in passports]

###############################
# Passport field validation 
###############################

def validate_required_fields(passport, required_fields):
    """
    Check if a passport contains all required keys.
    Returns True if all requires keys are present, False otherwise.
    """
    return all(k in passport for k in required_fields)


def validate_rules(passport, rules):
    """
    Check if all of the given rules validate for the given passport.
    """
    validated = [rule(passport[field]) for field, rule in rules.items()]
    return all(validated)


def validate_year(v, min_value, max_value):
    """
    Valid that the given value is a valid year format (4 digits)
    """
    m = regex_year.match(v)
    return m and min_value <= int(v) <= max_value


def validate_height(v):
    """
    Validate field hgt (Height) 
    a number followed by either cm or in: 
    If cm, the number must be at least 150 and at most 193.
    If in, the number must be at least 59 and at most 76.
    """
    m = regex_height.match(v)
    if not m:
        return False

    value = int(m.group(1))
    unit = m.group(2)

    return (unit == 'cm' and 150 <= value <= 193) \
        or (unit == 'in' and  59 <= value <= 76)


def validate_hair_color(v):
    """
    Validate field hcl (Hair Color)
    A # followed by exactly six characters 0-9 or a-f.
    """
    return regex_color.match(v)


def validate_eye_color(v):
    """
    Validate field ecl (Eye Color)
    Exactly one of: amb blu brn gry grn hzl oth.
    """
    return v in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')


def validate_pid(v):
    """
    Validate field pid (Passport ID) 
    A nine-digit number, including leading zeroes.
    """
    regex_pid = re.compile(r'^\d{9}$')
    return regex_pid.match(v)


def get_validation_rules():
    return {
        # Birth Year - four digits; at least 1920 and at most 2002.
        'byr': partial(validate_year, min_value=1920, max_value=2002),
        # Issue Year - four digits; at least 2010 and at most 2020.
        'iyr': partial(validate_year, min_value=2010, max_value=2020),
        # Expiration Year - four digits; at least 2020 and at most 2030.
        'eyr': partial(validate_year, min_value=2020, max_value=2030),
        'hgt': validate_height,
        'hcl': validate_hair_color,
        'ecl': validate_eye_color,
        'pid': validate_pid,
    }


##############
# Test cases
##############

def test_validate_year():
    assert validate_year('2000', 1900, 2020)
    assert validate_year('1900', 1900, 2020)
    assert validate_year('2020', 1900, 2020)
    assert not validate_year('200', 1900, 2020)
    assert not validate_year('1800', 1900, 2020)


def test_validate_height():
    assert validate_height('190cm')
    assert validate_height('70in')
    assert not validate_height('100in')
    assert not validate_height('100')
    assert not validate_height('100cm')


def test_validate_eye_color():
    assert validate_eye_color('amb')
    assert validate_eye_color('oth')
    assert not validate_eye_color('')
    assert not validate_eye_color('red')


def test_validate_hair_color():
    assert validate_hair_color('#123456')
    assert validate_hair_color('#123abc')
    assert validate_hair_color('#abcdef')
    assert not validate_hair_color('#12345')
    assert not validate_hair_color('123456')
    assert not validate_hair_color('red')
    assert not validate_hair_color('#123abz')
    assert not validate_hair_color('#123abcd')
    assert not validate_hair_color('123abc')


def test_validate_pid():
    assert validate_pid('000000001')
    assert not validate_pid('0123456789')


def test_all():
    "Runs all test cases"
    test_validate_year()
    test_validate_height()
    test_validate_hair_color()
    test_validate_eye_color()
    test_validate_pid()


if __name__ == "__main__":
    # Run unit tests
    test_all()

    # Read list of passports
    passports = read_passport_db()
    
    # Part 1: Check that all required fields are present
    passports_with_required_fields = [
        passport for passport in passports if validate_required_fields(passport, required_fields=required_fields)
    ]

    # Part 2: Check that all required fields pass the validation rules
    valid_passports = [
        passport 
        for passport 
        in passports_with_required_fields 
        if validate_rules(passport, rules=get_validation_rules())
    ]

    print(f'Total number passports: {len(passports)}')
    print(f'Number of passports with all required fields: {len(passports_with_required_fields)}')
    print(f'Number of passports where all fields validate: {len(valid_passports)}')
