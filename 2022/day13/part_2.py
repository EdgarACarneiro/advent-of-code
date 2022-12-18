import utils.file_handler
import enum
import functools

DIVIDER_PACKETS = [[[2]], [[6]]]


class Result(enum.Enum):
    IN_ORDER = 1
    NOT_IN_ORDER = -1
    INCONCLUSIVE = 0


def parse_list(entry: str) -> list[list | int]:
    res = []

    # First and last elements are []
    entry = entry[1:-1]

    while len(entry):
        if entry[0] == "[":
            # find the matching "]"
            open_brackets = 1
            close_brackets = 0
            i = 1

            while open_brackets != close_brackets:
                match entry[i]:
                    case "[":
                        open_brackets += 1
                    case "]":
                        close_brackets += 1
                i += 1

            next_val = entry[:i]
            res.append(parse_list(next_val))
        else:
            next_val = entry[: entry.find(",")] if entry.find(",") != -1 else entry
            res.append(int(next_val))

        entry = entry[len(next_val) + 1 :]

    return res


def is_pair_in_order(l1: list, l2: list) -> Result:
    """
    @returns 1 if given pairs are in order, -1 if they are not. It returns 0
    when the provided comparison doesn't let us conclude anything
    """
    if l1 == l2:
        return Result.INCONCLUSIVE

    try:
        for i in range(len(l1)):
            el1 = l1[i]
            el2 = l2[i]

            if isinstance(el1, int) and isinstance(el2, int):
                if el1 < el2:
                    return Result.IN_ORDER

                if el1 > el2:
                    return Result.NOT_IN_ORDER

                # Numbers are the same, continue
                continue

            if not isinstance(el1, list):
                el1 = [el1]
            elif not isinstance(el2, list):
                el2 = [el2]

            child_res = is_pair_in_order(el1, el2)
            # This means the comparison of the child lists allowed us to
            # conclude something
            if child_res != Result.INCONCLUSIVE:
                return child_res

    except IndexError:
        # l2 smaller than l1
        return Result.NOT_IN_ORDER

    # l1 was smaller than l2
    return Result.IN_ORDER


def comparison_fn(l1, l2) -> int:
    return is_pair_in_order(l1, l2).value


def main(input: list[str]) -> int:
    packets = []
    for p in DIVIDER_PACKETS:
        packets.append(p)

    for line in input:
        if not line.strip() == "":
            packets.append(parse_list(line.strip()))

    packets.sort(reverse=True, key=functools.cmp_to_key(comparison_fn))

    res = 1
    for i in range(len(packets)):
        if packets[i] in DIVIDER_PACKETS:
            res *= i + 1

    return res


def test():
    assert (
        main(
            """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]""".split(
                "\n"
            )
        )
        == 140
    )


if __name__ == "__main__":
    test()
    print(main(utils.file_handler.get_puzzle_input("13")))
