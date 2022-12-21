import utils.file_handler
import utils.timer

TUNING_MULTIPLIER = 4000000

TEST_LIMIT = 20
INPUT_LIMIT = 4000000


class Beacon:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def as_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)


class Sensor:
    x: int
    y: int
    range: int

    def __init__(self, x: int, y: int, closest_beacon: Beacon) -> None:
        self.x = x
        self.y = y

        # Manhattan distance between beacon and sensor
        self.range = abs(closest_beacon.x - x) + abs(closest_beacon.y - y)

    def get_x_range(self) -> tuple[int, int]:
        return (self.x - self.range, self.x + self.range)

    def in_range(self, pos: tuple[int, int]) -> bool:
        return abs(pos[0] - self.x) + abs(pos[1] - self.y) <= self.range

    def get_range_in_row(self, row: int) -> tuple[int, int]:
        y_diff = abs(self.y - row)
        old_range = self.get_x_range()
        new_range = (old_range[0] + y_diff, old_range[1] - y_diff + 1)

        return (-1, -1) if new_range[0] >= new_range[1] else new_range


def parse_line_input(line: str) -> tuple[Beacon, Sensor]:
    sensor_str, beacon_str = line.strip().split(":")

    # Parsing sensor
    sensor_str = sensor_str.replace("Sensor at x=", "")
    sensor_str = sensor_str.replace("y=", "")
    sx, sy = [int(val) for val in sensor_str.split(", ")]

    # Parsing beacon
    beacon_str = beacon_str.replace(" closest beacon is at x=", "")
    beacon_str = beacon_str.replace("y=", "")
    bx, by = [int(val) for val in beacon_str.split(", ")]
    beacon = Beacon(bx, by)

    return (beacon, Sensor(sx, sy, beacon))


def assert_ranges(ranges: list[tuple[int, int]], grid_limit: int) -> int:
    # this is fast since our list of sensors is small
    sorted_ranges = sorted([r for r in ranges if r != (-1, -1)])
    low_limit, high_limit = sorted_ranges[0]

    if low_limit > 0:
        # We found it
        return low_limit

    i = 1
    while i < len(sorted_ranges) and high_limit >= sorted_ranges[i][0]:
        high_limit = max(high_limit, sorted_ranges[i][1])
        i += 1

    if high_limit >= grid_limit:
        return -1

    # We found it!
    return high_limit


def main(input: list[str], grid_limit: int) -> int:
    sensors: list[Sensor] = []
    beacons: set = set()

    for line in input:
        b, s = parse_line_input(line)
        sensors.append(s)
        beacons.add(b.as_tuple())

    for y in range(0, grid_limit):
        if (
            x := assert_ranges([s.get_range_in_row(y) for s in sensors], grid_limit)
        ) != -1:
            return x * TUNING_MULTIPLIER + y

    raise Exception("Unable to find beacon")


def test():
    assert (
        main(utils.file_handler.get_puzzle_input("15", filename="test"), TEST_LIMIT)
        == 56000011
    )


if __name__ == "__main__":
    test()
    utils.timer.perf_time(
        lambda: print(
            main(utils.file_handler.get_puzzle_input("15"), INPUT_LIMIT),
        )
    )
