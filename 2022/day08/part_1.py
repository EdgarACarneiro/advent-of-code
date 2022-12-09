import utils.file_handler

# Note, this could be optimized on time if I were not creating new lists to be
# reused in the same function


def get_trees_seen(
    trees: str,
    seen_so_far: set[tuple[int, int]],
    row_num: int = -1,
    col_num: int = -1,
    is_row=True,
    reverse=False,
):
    tallest_so_far = -1

    generator = range(len(trees)) if not reverse else range(len(trees) - 1, -1, -1)

    for i in generator:
        if int(trees[i]) > tallest_so_far:
            tallest_so_far = int(trees[i])

            coords = (row_num, i) if is_row else (i, col_num)
            seen_so_far.add(coords)

            # Small optimisation
            if tallest_so_far == 9:
                return seen_so_far


def main(input: list[str]) -> int:
    trees_seen = set()

    # Horizontal scans
    for i in range(len(input)):
        # left to right scan
        get_trees_seen(input[i].strip(), trees_seen, row_num=i)
        # right to left scan
        get_trees_seen(input[i].strip(), trees_seen, row_num=i, reverse=True)

    # Vertical scans
    for i in range(len(input[0].strip())):
        col = ""
        for row in input:
            col += row[i]

        # top to bottom scan
        get_trees_seen(col, trees_seen, col_num=i, is_row=False)
        # bottom to top scan
        get_trees_seen(col, trees_seen, col_num=i, is_row=False, reverse=True)

    return len(trees_seen)


def test():
    assert (
        main(
            """30373
25512
65332
33549
35390""".split(
                "\n"
            )
        )
        == 21
    )


if __name__ == "__main__":
    test()
    print(main(utils.file_handler.get_puzzle_input("08")))
