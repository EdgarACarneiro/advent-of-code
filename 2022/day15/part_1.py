import utils.file_handler
import utils.timer

TEST_ROW = 10
GOAL_ROW = 2000000


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

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.range})"


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


def main(input: list[str], row: int) -> int:
    sensors: list[Sensor] = []
    beacons: set = set()

    # Limits for row iteration
    b0, s0 = parse_line_input(input[0])
    sensors.append(s0)
    beacons.add(b0.as_tuple())

    s0_range: tuple[int, int] = s0.get_x_range()
    min_x = min(b0.x, s0_range[0])
    max_x = max(b0.x, s0_range[1])

    for i in range(1, len(input)):
        b, s = parse_line_input(input[i])
        sensors.append(s)
        beacons.add(b.as_tuple())

        # Update limits
        s_range: tuple[int, int] = s.get_x_range()
        min_x = min(min_x, b.x, s_range[0])
        max_x = max(max_x, b.x, s_range[1])

    res = 0

    for x in range(min_x, max_x + 1):
        if (x, row) in beacons:
            continue

        for s in sensors:
            if s.in_range((x, row)):
                res += 1
                break

    return res


def test():
    assert (
        main(utils.file_handler.get_puzzle_input("15", filename="test"), TEST_ROW) == 26
    )


if __name__ == "__main__":
    test()
    utils.timer.perf_time(
        lambda: print(
            main(utils.file_handler.get_puzzle_input("15"), GOAL_ROW),
        )
    )