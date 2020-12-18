import os
import re

test_str = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""


def read_file(fname='input.txt'):
    fname = os.path.join(os.path.dirname(__file__), fname)
    with open(fname, 'r') as fp:
        return fp.read().strip()


def parse_input(s):
    regex_rule = re.compile(r'(.+): (\d+\-\d+) or (\d+\-\d+)')
    regex_ticket = re.compile(r'[\d,]+')

    rules = []
    tickets = []

    for line in s.strip().split('\n'):
        match_rule = regex_rule.match(line)
        match_ticket = regex_ticket.match(line)
        if match_rule:
            for interval in (match_rule.group(2), match_rule.group(3)):
                rules.append([int(num) for num in interval.split('-')])
        elif match_ticket:
            tickets.append([int(num) for num in line.split(',')])

    return rules, tickets


def in_interval(num, interval):
    start, end = interval
    return start <= num <= end


def check_tickets(rules, tickets):
    invalid = []  # collect invalid numbers across all tickets

    for ticket in tickets:
        for num in ticket:
            if not any(in_interval(num, interval) for interval in rules):
                invalid.append(num)
    return sum(invalid)


def test():
    rules, tickets = parse_input(test_str)
    print(rules)
    print(tickets)
    assert check_tickets(rules, tickets) == 71


def main():
    contents = read_file()
    rules, tickets = parse_input(contents)
    print('Part 1')
    result = check_tickets(rules, tickets)
    print(result)
    

if __name__ == "__main__":
    test()
    main()
