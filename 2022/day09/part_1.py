import utils.file_handler
import enum


class Direction(enum.Enum):
    RIGHT = "R"
    LEFT = "L"
    UP = "U"
    DOWN = "D"


class Coords:

    x: int
    y: int

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def get_position(self):
        return (self.x, self.y)

    def squared_distance(self, coords) -> int:
        x_diff = coords.x - self.x
        y_diff = coords.y - self.y
        return x_diff * x_diff + y_diff * y_diff

    def move(self, direction: Direction) -> None:
        match direction:
            case Direction.RIGHT:
                self.x += 1
            case Direction.LEFT:
                self.x -= 1
            case Direction.UP:
                self.y += 1
            case Direction.DOWN:
                self.y -= 1
            case _:
                raise Exception(f"Unknown move {direction}")


class Tail(Coords):
    def move(self, head: Coords) -> None:
        if self.squared_distance(head) <= 2:
            # Stay put -> Head is next to tail or in diagonal
            return

        # Update x
        if x_diff := head.x - self.x:
            if x_diff > 0:
                self.x += 1
            else:
                self.x -= 1

        # Update y
        if y_diff := head.y - self.y:
            if y_diff > 0:
                self.y += 1
            else:
                self.y -= 1


def main(input: list[str]) -> int:
    visited_positions: set = set()
    head = Coords(0, 0)
    tail = Tail(0, 0)

    for line in input:
        direction, moves = line.split(" ")

        for _ in range(int(moves)):
            head.move(Direction(direction))
            tail.move(head)
            visited_positions.add(tail.get_position())

    return len(visited_positions)


def test():
    assert (
        main(
            """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""".split(
                "\n"
            )
        )
        == 13
    )


if __name__ == "__main__":
    test()
    print(main(utils.file_handler.get_puzzle_input("09")))
