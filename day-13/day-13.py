import os


def read_file(fname='input.txt'):
    fname = os.path.join(os.path.dirname(__file__), fname)
    with open(fname, 'r') as fp:
        return fp.read().strip()


def parse_input(contents):
    departure, bus_ids = contents.strip().split('\n')
    departure = int(departure)
    bus_ids = [int(bus) for bus in bus_ids.split(',') if bus != 'x']

    return departure, bus_ids


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
        

def test_all():
    test_str = """939
7,13,x,x,59,x,31,19"""
    departure, bus_ids = parse_input(test_str)
    bus, wait = pick_bus(departure, bus_ids)
    assert bus * wait == 295

    
def main():

    s = read_file()
    departure, bus_ids = parse_input(s)

    # Q: What is the ID of the earliest bus you can take to the airport multiplied
    #    by the number of minutes you'll need to wait for that bus?
    print('Part 1')
    bus, wait = pick_bus(departure, bus_ids)
    print(bus * wait)


if __name__ == "__main__":
    test_all()
    main()