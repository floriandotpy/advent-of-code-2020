#!/env/python3
"""
Read a list of passwords including individual password policies
and count how many passwords pass their given policy.
"""

import re
from collections import Counter

regex = re.compile(r"(\d+)\-(\d+)\s(.):\s(.+)")


def read_password_db(fname='input.txt'):
    """
    Read password db entries from file `fname` and return a list of dictionaries.
    """
    with open(fname) as fp:
        matches = [regex.match(line) for line in fp.readlines()]
            
    passwords = [{
        'num_1': int(m.group(1)),
        'num_2': int(m.group(2)),
        'character': m.group(3),
        'password': m.group(4)
    } for m in matches]
    
    return passwords


def password_is_valid_1(password, character, num_1, num_2):
    """
    Check if the given password passes policy 1.

    The policy is considered passed if `character` appears in `password`
    at least `num_1` times and at most `num_2` times.

    Returns True if policy is passed, False otherwise.
    """
    counter = Counter(password)
    character_count = counter.get(character, 0)
    return num_1 <= character_count <= num_2


def password_is_valid_2(password, character, num_1, num_2):
    """
    Check if the given password passes the given policy 2.

    The policy is considered passed if `character` appears in `password`
    either at position `num_1` or at position `num_2` but not at both positions.
    Note: Position is 1-based.

    Example:
      num_1 = 1
      num_2 = 3 
      character = a
      password = abcde
      -> Passed: Position 1 contains a and position 3 does not.

    Returns True if policy is passed, False otherwise.
    """
    char_1 = password[num_1 - 1]
    char_2 = password[num_2 - 1]

    return (char_1 == character or char_2 == character) and char_1 != char_2


if __name__ == "__main__":
    password_db = read_password_db()

    print('Part 1')
    passes = [password_is_valid_1(**kwargs) for kwargs in password_db]
    passes = Counter(passes)
    print(f'Out of {len(password_db)} password in total, {passes[True]} pass the password policy')

    print('Part 2')
    passes = [password_is_valid_2(**kwargs) for kwargs in password_db]
    passes = Counter(passes)
    print(f'Out of {len(password_db)} password in total, {passes[True]} pass the password policy')
