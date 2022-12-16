import utils.file_handler
from collections.abc import Callable
from typing import Self

ROUNDS = 10000
WORRY_LEVEL_DIVIDER = 3


class Monkey:

    items: list[int]
    operation: Callable[[int], int]
    test: int
    true_monkey: int
    false_monkey: int
    num_inspections: int

    def __init__(self, description: list[str]) -> None:
        self.num_inspections = 0
        assert len(description) == 6

        # Extract starting items
        starting_items = description[1].strip()
        starting_items = starting_items.replace("Starting items: ", "")
        self.items = [int(item) for item in starting_items.split(", ")]

        # Extract operation
        operation = description[2].strip()
        operation = operation.replace("Operation: new = old ", "")
        match operation.split(" "):
            case ["*", val]:
                self.operation = lambda x: x * (x if val == "old" else int(val))
            case ["+", val]:
                self.operation = lambda x: x + (x if val == "old" else int(val))
            case op:
                raise Exception(f"Unknown operation {op}")

        # Extract test number
        self.test = int(description[3].strip().split(" ")[-1])

        # Extract monkeys for redirection of item
        self.true_monkey = int(description[4].strip()[-1])
        self.false_monkey = int(description[5].strip()[-1])

    def receive_item(self, item: int):
        self.items.append(item)

    def send_item(self, item: int, new_val_item: int, receiver: Self):
        self.items.remove(item)
        receiver.receive_item(new_val_item)

    def inspected(self):
        self.num_inspections += 1


def main(input: list[str]) -> int:
    # Parse the monkeys
    monkeys: list[Monkey] = []
    for i in range(0, len(input), 7):
        monkeys.append(Monkey(input[i : i + 6]))

    # The problem is that the now the numbers will become to big
    # However, by finding the least common multiple,, we find a number in which
    # we know all tests will get the same value = 0. This means than that for
    # any test t, t mod lcm = 0. Hence, we know that for any number x, if we do
    # x = x mod lcm, the new x value will return the value when computing x mod t.
    lcm = 1
    for m in monkeys:
        lcm *= m.test

    # run the rounds
    for i in range(ROUNDS):
        for monkey in monkeys:
            # Monkey turn
            while len(monkey.items):
                monkey.inspected()
                og_item = monkey.items[0]
                item = monkey.operation(og_item)
                item %= lcm

                monkey.send_item(
                    og_item,
                    item,
                    monkeys[
                        monkey.true_monkey
                        if not item % monkey.test
                        else monkey.false_monkey
                    ],
                )

    max1 = 0
    max2 = 0
    for monkey in monkeys:
        if monkey.num_inspections > max1:
            max2 = max1
            max1 = monkey.num_inspections
        elif monkey.num_inspections > max2:
            max2 = monkey.num_inspections

    return max1 * max2


def test():
    assert (
        main(
            """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1""".split(
                "\n"
            )
        )
        == 2713310158
    )


if __name__ == "__main__":
    test()
    print(main(utils.file_handler.get_puzzle_input("11")))
