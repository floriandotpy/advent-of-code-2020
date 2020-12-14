"""
Implementation notes:

Part 2 was annoying. It wasn't trivially solvable by implementation.
You needed a bit of math, and in particular you needed to know which
kind of math.

https://en.wikipedia.org/wiki/Chinese_remainder_theorem#Search_by_sieving
"""

import os


def read_file(fname='input.txt'):
    fname = os.path.join(os.path.dirname(__file__), fname)
    with open(fname, 'r') as fp:
        return fp.read().strip()


def parse_input(contents):
    departure, bus_ids = contents.strip().split('\n')
    departure = int(departure)
    busses = {
        offset: int(bus)
        for offset, bus
        in enumerate(bus_ids.split(','))
        if bus != 'x'
    }

    return departure, busses


def next_arrival(departure, bus):
    # How many minutes since the bus was last here?
    remainder = departure % bus
    # How many minutes till next arrival
    next_arrival = bus - remainder
    return next_arrival


def pick_bus(departure, bus_ids):
    arrivals = [(bus, next_arrival(departure, bus)) for bus in bus_ids]
    next_bus, wait_minutes = min(arrivals, key=lambda tup: tup[1])
    return next_bus, wait_minutes


def generate_arrivals(t, bus_ids, initial_offsets):
    while True:
        arrivals = [
            next_arrival(t, bus) - t + initial
            for bus, initial 
            in zip(bus_ids, initial_offsets)
        ]
        t += 1
        yield t, arrivals


def find_t(busses):
    """
    Implementation of Chinese Remainder Problem (by sieving)
    https://en.wikipedia.org/wiki/Chinese_remainder_theorem#Search_by_sieving
    """
    busses = [(offset, time) for offset, time in busses.items()] 
    
    t, step = 0, busses[0][1]
    for offset, time in busses[1:]:
        while (t + offset) % time != 0:
            t += step

        step *= time

    return t


def test_all():
    test_str = """939
    7,13,x,x,59,x,31,19"""
    departure, busses = parse_input(test_str)
    bus_ids = list(busses.values())
    bus, wait = pick_bus(departure, bus_ids)
    assert bus * wait == 295

    t = find_t(busses)
    assert t == 1068781, t


def main():

    s = read_file()
    departure, busses = parse_input(s)
    bus_ids = list(busses.values())

    # Q: What is the ID of the earliest bus you can take to the airport
    #    multiplied by the number of minutes you'll need to wait for that bus?
    print('Part 1')
    bus, wait = pick_bus(departure, bus_ids)
    print(bus * wait)

    # Q: What is the earliest timestamp such that all of the listed bus IDs
    #    depart at offsets matching their positions in the list?
    print('Part 2')
    t = find_t(busses)
    print(t)


if __name__ == "__main__":
    test_all()
    main()
