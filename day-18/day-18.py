import os
import re

regex_number = re.compile(r'\d')


def read_file(fname='input.txt'):
    fname = os.path.join(os.path.dirname(__file__), fname)
    with open(fname, 'r') as fp:
        return fp.read().strip().split('\n')


def find_matching_parenthesis(expr, index_opening):
    index = index_opening
    opening_count = 0
    while index < len(expr):
        if expr[index] == '(':
            opening_count += 1
        if expr[index] == ')':
            opening_count -= 1

        if opening_count == 0:
            # found matching
            return index
        index += 1

    # no matching closing parenthesis found
    return -1


def eval(expr):
    # remove whitespace
    expr = expr.replace(' ', '')
    
    result = None
    op = None
    index = 0

    # walk expression from left to right. no enumerate so that we may skip by setting index
    while index < len(expr):
        c = expr[index]

        # op sign? remember now, evaluate after second operand (number) has been encountered
        if c == '+':
            op = '+'
            index += 1
            continue
        if c == '*':
            op = '*'
            index += 1
            continue

        # parenthesis? first evaluate sub expression
        if c == '(':
            # find matching parenthesis
            index_closing = find_matching_parenthesis(expr, index)
            operand = eval(expr[index+1:index_closing])
            index = index_closing
        elif regex_number.match(c):
            operand = int(c)

        # optional: if this was the second (or n-th, for n>0) operand, evaluate with previous operand
        if op is None:
            # no op known yet. remember operand for next iteration
            result = operand
        elif op is '+':
            result += operand
        elif op is '*':
            result *= operand

        index += 1

    return result


def test_find_matching_parenthesis():
    assert find_matching_parenthesis('(123)', 0) == 4

    # parenthesis in sequence
    assert find_matching_parenthesis('(123)(67)', 0) == 4
    assert find_matching_parenthesis('(123)(67)', 5) == 8

    # sequence with op in between
    assert find_matching_parenthesis('(12)+(67)', 5) == 8
    assert find_matching_parenthesis('(12)+(67)', 0) == 3

    # nesting
    assert find_matching_parenthesis('((23)(67))', 0) == 9
    assert find_matching_parenthesis('((23)(67))', 1) == 4
    assert find_matching_parenthesis('((23)(67))', 5) == 8


def test():
    test_find_matching_parenthesis()

    assert 71 == eval('1 + 2 * 3 + 4 * 5 + 6')
    assert 26 == eval('2 * 3 + (4 * 5)')
    assert 437 == eval('5 + (8 * 3 + 9 + 3 * 4 * 3)')
    assert 12240 == eval('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))')
    assert 13632 == eval('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2')


def main():
    expressions = read_file()

    print('Part 1')
    # Q: Evaluate the expression on each line of the homework; 
    #    what is the sum of the resulting values?
    result = sum([
        eval(expr) for expr in expressions
    ])
    print(result)


if __name__ == "__main__":
    test()
    main()
