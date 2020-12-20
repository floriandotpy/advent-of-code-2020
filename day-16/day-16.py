import os
import re
from collections import defaultdict
from functools import reduce

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

test_str_2 = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
"""


def read_file(fname='input.txt'):
    fname = os.path.join(os.path.dirname(__file__), fname)
    with open(fname, 'r') as fp:
        return fp.read().strip()


def parse_input(s):
    regex_rule = re.compile(r'(.+): (\d+\-\d+) or (\d+\-\d+)')
    regex_ticket = re.compile(r'[\d,]+')

    rules = defaultdict(list)
    tickets = []

    for line in s.strip().split('\n'):
        match_rule = regex_rule.match(line)
        match_ticket = regex_ticket.match(line)
        if match_rule:
            rule_name = match_rule.group(1)
            for interval in (
                match_rule.group(2),
                match_rule.group(3)
                ):
                rules[rule_name].append([int(num) for num in interval.split('-')])
        elif match_ticket:
            tickets.append([int(num) for num in line.split(',')])

    return rules, tickets


def in_interval(num, interval):
    start, end = interval
    return start <= num <= end


def check_tickets(rules, tickets):
    invalid_numbers = []
    valid_tickets = []
    
    # flatten all rules into one single list of intervals
    all_rules = []
    for intervals in rules.values():
        all_rules.extend([intervals[0], intervals[1]])

    for ticket in tickets:
        ticket_valid = True
        for num in ticket:
            if not any(
                in_interval(num, interval)
                for interval in all_rules
                ):
                invalid_numbers.append(num)
                ticket_valid = False
        if ticket_valid:
            valid_tickets.append(ticket)
            
    return sum(invalid_numbers), valid_tickets


def determine_fields(numbers, rules):
    fields = set()
    for rule_name, (interval_1, interval_2) in rules.items():
        if all(
            in_interval(num, interval_1)
            or in_interval(num, interval_2)
            for num in numbers
            ):
            fields.add(rule_name)
    return fields


def match_fields(tickets, rules):
    nearby = tickets[1:]
   
    # Find all possible mappings of field index -> field names (plural!)
    mapping = []
    for column in zip(*nearby):
        field_names = determine_fields(column, rules)
        mapping.append(field_names)  # list index matches field index

    # Reduce to distinct and unique mapping of field index -> field name (singular)
    final_mapping = dict()
    while len(final_mapping) < len(mapping):
        for idx, field_names in enumerate(mapping):
            # remove all mappings that have been assigned alredy
            field_names -= set(final_mapping.values())
            
            # distinct mapping found
            if len(field_names) == 1:
                field = field_names.pop()
                final_mapping[idx] = field

    return final_mapping


def test():
    # part 1
    rules, tickets = parse_input(test_str)
    answer, _ = check_tickets(rules, tickets)
    assert answer == 71

    # part 2
    rules_2, tickets_2 = parse_input(test_str_2)
    _, valid_tickets = check_tickets(rules_2, tickets_2)
    assert determine_fields([3, 15, 5], rules_2) == {'row'}, determine_fields([3, 15, 5], rules_2)
    assert determine_fields([9, 1, 14], rules_2) == {'row', 'class'}, determine_fields([9, 1, 14], rules_2)
    assert determine_fields([18, 5, 9], rules_2) == {'row', 'seat', 'class'}, determine_fields([18, 5, 9], rules_2)
    matched = match_fields(valid_tickets, rules_2)
    assert matched == {0: 'row', 1: 'class', 2: 'seat'}
    

def main():
    contents = read_file()
    rules, tickets = parse_input(contents)
    print('Part 1')
    result, valid_tickets = check_tickets(rules, tickets)
    print(result)

    print('Part 2')
    mapping = match_fields(valid_tickets, rules)
    indices = [idx for idx, field in mapping.items() if field.startswith('departure')]
    my_ticket = tickets[0]
    values = [my_ticket[idx] for idx in indices]
    result = reduce(lambda a, b: a * b, values)
    print(result)
    

if __name__ == "__main__":
    test()
    main()
