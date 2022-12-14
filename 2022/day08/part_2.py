import utils.file_handler


class TreeScore:

    up: int
    down: int
    left: int
    right: int

    def __init__(self) -> None:
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0

    def get_score(self) -> int:
        return self.up * self.down * self.left * self.right

    def __str__(self):
        return f"{self.right}x{self.left}x{self.up}x{self.down}={self.get_score()}"


def get_list_scenic_score(
    row: str,
    score_row: list[list[TreeScore]],
    direction: str,
    get_max_score: bool = False,
):
    max_score = 0 if get_max_score else None

    for i in range(len(row)):
        j = i - 1
        while j >= 0:
            # TODO: this could be optimised in a DP fashion, if we consider that
            # if a tree i is bigger then tree i-1, then it can always see all
            # the trees tree i-1 can see.
            setattr(score_row[i], direction, getattr(score_row[i], direction) + 1)
            if int(row[i]) <= int(row[j]):
                break
            j -= 1

        if get_max_score:
            max_score = max(max_score, score_row[i].get_score())

    return max_score


def main(input: list[str]) -> int:
    # Initialize tree score matrix
    scores = []
    for _ in range(len(input)):
        row = []
        for _ in range(len(input[0].strip())):
            row.append(TreeScore())
        scores.append(row)

    # Horizontal scans
    for i in range(len(input)):
        # left to right scan
        get_list_scenic_score(input[i].strip(), scores[i], "right")

        # right to left scan
        get_list_scenic_score(
            list(reversed(input[i].strip())), list(reversed(scores[i])), "left"
        )

    # In the last scan lets get the max score
    max_score = 0

    # Vertical scans
    for i in range(len(input[0].strip())):
        col = ""
        col_scores = []
        for j in range(len(input)):
            col += input[j][i]
            col_scores.append(scores[j][i])

        # top to bottom scan
        get_list_scenic_score(col, col_scores, "up")

        # since this is the last scan lets also get the max
        # bottom to top scan
        score = get_list_scenic_score(
            list(reversed(col)),
            list(reversed(col_scores)),
            "down",
            get_max_score=True,
        )

        max_score = max(score, max_score)

    return max_score


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
        == 8
    )


if __name__ == "__main__":
    test()
    print(main(utils.file_handler.get_puzzle_input("08")))
