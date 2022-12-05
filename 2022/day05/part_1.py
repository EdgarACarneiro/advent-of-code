import utils.file_handler


class Instruction:
    src_crate: int
    dest_crate: int
    quantity: int

    def __init__(self, instruction: str):
        # Cleaning not needed stuff
        res = instruction.replace("move ", "")
        res = res.replace("from ", "")
        res = res.replace("to ", "")
        res = res.split(" ")

        self.quantity = int(res[0])
        self.src_crate = int(res[1]) - 1
        self.dest_crate = int(res[2]) - 1

    def __str__(self):
        return (
            f"Move {self.quantity} from {self.src_crate + 1} to {self.dest_crate + 1}"
        )


class CrateStacks:

    stacks: list[list[str]] = []

    def __init__(self, input: list[str]):
        # Last line indicates the number of columns, lets get that first
        num_stacks_list = input[-1].strip().split("   ")
        num_stacks = int(num_stacks_list[-1])
        for _ in range(num_stacks):
            self.stacks.append([])

        # Full filling crates from top to bottom
        for row in reversed(input[0:-1]):
            for i in range(num_stacks):
                crate = row[i * 4 : i * 4 + 3][1]
                if crate != " ":
                    self.stacks[i].append(crate)

    def apply(self, instruction: Instruction):
        temp = self.stacks[instruction.src_crate][-1 : -instruction.quantity - 1 : -1]

        self.stacks[instruction.src_crate] = self.stacks[instruction.src_crate][
            : -instruction.quantity
        ]
        self.stacks[instruction.dest_crate] += temp

    def get_top_of_stacks(self):
        return "".join([stack[-1] for stack in self.stacks if len(stack)])

    def __str__(self):
        return "".join(f"{s}\n" for s in self.stacks)


def main(input: list[str]) -> int:
    # The new line is the separator between the create initial design and
    # the instructions
    separator = 0
    for i in range(0, len(input)):
        if input[i].strip() == "":
            separator = i
            break

    crate_stacks = CrateStacks(input[0:separator])

    for i in range(separator + 1, len(input)):
        crate_stacks.apply(Instruction(input[i]))

    return crate_stacks.get_top_of_stacks()


def test():
    test_input = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""
    assert main(test_input.split("\n")) == "CMZ"


if __name__ == "__main__":
    test()
    print(main(utils.file_handler.get_puzzle_input("05")))
