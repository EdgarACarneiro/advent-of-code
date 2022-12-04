import utils.file_handler


class Range:

    lb: int
    up: int

    def __init__(self, lb, ub):
        self.lb = int(lb)
        self.ub = int(ub)

    @staticmethod
    def from_str(range_str: str):
        return Range(*range_str.split("-"))

    def intersection(self, other):
        if self.lb > other.ub or self.ub < other.lb:
            return None

        return Range(max(self.lb, other.lb), min(self.ub, other.ub))

    def __eq__(self, other):
        return (self.lb, self.ub) == (other.lb, other.ub)

    def __str__(self):
        return f"{self.lb}-{self.ub}"


def main(input: list[str]) -> int:
    res = 0

    for line in input:
        range1, range2 = line.strip().split(",")

        if Range.from_str(range1).intersection(Range.from_str(range2)):
            res += 1

    return res


def test():
    test_input = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""
    assert main(test_input.split("\n")) == 4


if __name__ == "__main__":
    test()
    print(main(utils.file_handler.get_puzzle_input("04")))
