import utils.file_handler

INITIAL_COORD = (500, 0)


# Returns the last found rock before reaching the void
def parse_rocks(line: str, rocks: set[tuple[int, int]]) -> int:
    last_rock = 0
    values = line.strip().split(" -> ")

    for i in range(0, len(values) - 1):
        x1, y1 = values[i].split(",")
        x2, y2 = values[i + 1].split(",")
        last_rock = max(last_rock, int(y1), int(y2))

        if x1 == x2:
            y1 = int(y1)
            y2 = int(y2)
            for y in range(min(y1, y2), max(y1, y2) + 1):
                rocks.add((int(x1), y))
        else:
            x1 = int(x1)
            x2 = int(x2)
            for x in range(min(x1, x2), max(x1, x2) + 1):
                rocks.add((x, int(y1)))

    return last_rock


# Returns the position of the sand grain when still
def let_sand_fall(
    curr_pos: tuple[int, int],
    rocks: set[tuple[int, int]],
    sand: set[tuple[int, int]],
    floor_lvl: int,
) -> tuple[int, int]:
    if curr_pos[1] + 1 == floor_lvl:
        sand.add(curr_pos)
        return curr_pos

    # if curr_pos not in rocks and curr_pos not in sand
    new_pos = (curr_pos[0], curr_pos[1] + 1)
    if new_pos not in rocks and new_pos not in sand:
        return let_sand_fall(new_pos, rocks, sand, floor_lvl)

    new_pos = (curr_pos[0] - 1, curr_pos[1] + 1)
    if new_pos not in rocks and new_pos not in sand:
        return let_sand_fall(new_pos, rocks, sand, floor_lvl)

    new_pos = (curr_pos[0] + 1, curr_pos[1] + 1)
    if new_pos not in rocks and new_pos not in sand:
        return let_sand_fall(new_pos, rocks, sand, floor_lvl)

    sand.add(curr_pos)
    return curr_pos


def main(input: list[str]) -> int:
    last_rock = 0

    rocks = set()
    for line in input:
        last_rock = max(last_rock, parse_rocks(line, rocks))
    floor_lvl = last_rock + 2

    sand = set()
    while INITIAL_COORD not in sand:
        let_sand_fall(INITIAL_COORD, rocks, sand, floor_lvl)

    return len(sand)


def test():
    assert (
        main(
            """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9""".split(
                "\n"
            )
        )
        == 93
    )


if __name__ == "__main__":
    test()
    print(main(utils.file_handler.get_puzzle_input("14")))
