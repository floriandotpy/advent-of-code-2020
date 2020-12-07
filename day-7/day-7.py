import os
import re

test_str = """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""

regex_subcontent = re.compile(r'(\d+) (.+) bags?')


def read_rules(fname='input.txt'):
    # always find file, no matter from where this script is called
    fname = os.path.join(
        os.path.dirname(__file__),
        fname
    )

    with open(fname) as fp:
        rules_list = [
            parse_rule(line)
            for line
            in fp.read().strip().split('\n') 
        ]

    return {k: v for k, v in rules_list}


def parse_rule(rule_str):

    outer_color, content = rule_str.split(' bags contain ')

    items = []
    if 'no other bags' not in content:
        for sub_content in content.split(', '):
            sub_content.replace('.', '').strip()
            match = regex_subcontent.match(sub_content)
            items.append({
                'count': int(match.group(1)),
                'color': match.group(2)
            })

    return outer_color, items

    
def build_inverse_rules(rules):
    # map from inner_color -> list of colors it can be contained in
    inverse_rules = {}

    for outer_color, items in rules.items():
        for item in items:
            inner_color = item['color']

            inverse_rules[inner_color] = inverse_rules.get(inner_color, set())
            inverse_rules[inner_color].add(outer_color)

    return inverse_rules


def count_outer_colors(color, inverse_rules, acc_result=None):
    """
    Counts in how many differently colored bags a bag of the color `color` can be contained.
    """

    # accumulator variable: accumulate result during recursive calls
    acc_result = acc_result or set()

    # which bags can contain the color `color`?
    outer_colors = inverse_rules.get(color)

    # this color can only occur as the outermost bag? recursion end.
    if not outer_colors:
        return set()

    # `color` can be contained in (potentially) multiple different color
    for outer_color in outer_colors:

        # remember color in accumulator (for final result)
        acc_result.add(outer_color)

        # recursion: look one level of bags higher
        recurse_result = count_outer_colors(outer_color, inverse_rules)
        acc_result.update(recurse_result)
    
    return acc_result


def count_inner_bags(outer_bag, rules):
    """
    Count how many bags a bag of the color `outer_bag` contains in total.
    """
    inner_bags = rules[outer_bag]

    num_inner_bags = [
        bag['count'] * (1 + count_inner_bags(bag['color'], rules))
        for bag in inner_bags
    ]
    
    return sum(num_inner_bags)


def test_all():

    rules = [
        parse_rule(line)
        for line
        in test_str.strip().split('\n')
    ]
    rules = {k: v for k, v in rules}

    inverse_rules = build_inverse_rules(rules)
    actual = len(count_outer_colors('shiny gold', inverse_rules))
    assert actual == 4

    num_inner_bags = count_inner_bags('shiny gold', rules)
    print('actual: ', num_inner_bags)
    assert num_inner_bags == 32


if __name__ == "__main__":
    test_all()

    rules = read_rules()    
    inverse_rules = build_inverse_rules(rules)

    print('Part 1')
    result_1 = count_outer_colors('shiny gold', inverse_rules)
    print(len(result_1))

    print('Part 2')
    result_2 = count_inner_bags('shiny gold', rules)
    print(result_2)
