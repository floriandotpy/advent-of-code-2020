from collections import defaultdict


def play(sequence, final_turn=2020, log_every=1_000_000):

    history = defaultdict(list)
    turn = 1
    number = None
    while turn <= final_turn:
        if turn % log_every == 0:
            print(f'...turn {turn}')

        if len(sequence):
            # still feeding of initial sequence
            number = sequence.pop(0)
        elif len(history[number]) == 1:
            # number has been spoken once -> new number is 0
            number = 0
        else:
            # number spoken before: what was distance of previous 2 utterances?
            number = history[number][-1] - history[number][-2] 
        history[number].append(turn)
        turn += 1

    return number


def test():
    # Tests part 1
    assert play([0, 3, 6]) == 436
    assert play([1, 3, 2]) == 1
    assert play([2, 1, 3]) == 10
    assert play([1, 2, 3]) == 27
    assert play([2, 3, 1]) == 78
    assert play([3, 2, 1]) == 438
    assert play([3, 1, 2]) == 1836


def main():
    print('Part 1')
    result = play([0,3,1,6,7,5])
    print(result)

    print('Part 2')
    result = play([0,3,1,6,7,5], final_turn=30_000_000)
    print(result)


if __name__ == "__main__":
    test()
    main()
