import utils.file_handler

ASCII_LOWERCASE_LETTERS_START_VAL = 96
ASCII_UPPERCASE_LETTERS_START_VAL = 38


def get_item_val(item: str) -> int:
    return ord(item) - (
        ASCII_LOWERCASE_LETTERS_START_VAL
        if item.islower()
        else ASCII_UPPERCASE_LETTERS_START_VAL
    )


def get_common_item_triple_rucksack(rucksacks: list[list[str]]) -> int:
    assert len(rucksacks) == 3

    # shared items first rucksack
    shared_items = set(rucksacks[0].strip())

    # shared items between all rucksacks
    shared_items = shared_items.intersection(
        set(rucksacks[1].strip()),
        set(rucksacks[2].strip()),
    )

    assert len(shared_items) == 1
    return get_item_val(shared_items.pop())


def main(input: list[str]) -> str:
    return sum(
        get_common_item_triple_rucksack(input[i : i + 3])
        for i in range(0, len(input), 3)
    )


def test():
    test_input = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""
    assert main(test_input.split("\n")) == 70


if __name__ == "__main__":
    test()
    print(main(utils.file_handler.get_puzzle_input("03")))
