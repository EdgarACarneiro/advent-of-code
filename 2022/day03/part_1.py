import utils.file_handler

ASCII_LOWERCASE_LETTERS_START_VAL = 96
ASCII_UPPERCASE_LETTERS_START_VAL = 38


def get_item_val(item: str):
    return ord(item) - (
        ASCII_LOWERCASE_LETTERS_START_VAL
        if item.islower()
        else ASCII_UPPERCASE_LETTERS_START_VAL
    )


def get_rucksack_shared_items_value(line: str):
    # Different behaviour if 1st or 2nd compartment
    middle_point = len(line) // 2
    hashmap = {}
    shared_items_val = 0

    for i in range(len(line)):
        # 1st compartment - put in hashmap
        if i < middle_point:
            # Value marks if item already appeared
            hashmap[line[i]] = False

        # 2nd compartment verify if any object is in hashmap
        elif line[i] in hashmap and not hashmap[line[i]]:
            shared_items_val += get_item_val(line[i])
            hashmap[line[i]] = True

    return shared_items_val


def main(input: list[str]) -> int:
    return sum(
        get_rucksack_shared_items_value(line.strip())
        for line in input
        if len(line.strip())
    )


def test():
    test_input = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""
    assert main(test_input.split("\n")) == 157


if __name__ == "__main__":
    test()
    print(main(utils.file_handler.get_puzzle_input("03")))
