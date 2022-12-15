import utils.file_handler
import abc

SIGNAL_STRENGTH_START = 20
SIGNAL_STRENGTH_LOOP = 40


class Instruction(abc.ABC):

    duration: int
    value: int

    def __init__(self, duration: int, value: int) -> None:
        self.duration = duration
        self.value = value

    def tick(self) -> None:
        self.duration -= 1

    def has_finished(self) -> bool:
        return self.duration == 0

    def get_value(self) -> int:
        return self.value


class Noop(Instruction):
    def __init__(self) -> None:
        super().__init__(1, 0)


class Addx(Instruction):
    def __init__(self, value: int) -> None:
        super().__init__(2, value)


def parse_instruction(instruction: str) -> Instruction:
    match instruction.strip().split(" "):
        case ["noop"]:
            return Noop()
        case ["addx", val]:
            return Addx(int(val))
        case unknown:
            raise Exception(f"Unknown instruction {unknown}")


def main(input: list[str]) -> int:

    cycle = 1
    total_score = 0
    signal_score = 1
    current_instruction: tuple[int, Instruction] = (0, parse_instruction(input[0]))

    while True:
        # Process next instruction if current one has finished
        if current_instruction[1].has_finished():
            # Process finished instruction
            signal_score += current_instruction[1].get_value()

            # We processed all instructions and there isn't any instruction
            # being processed
            new_idx = current_instruction[0] + 1
            if new_idx >= len(input):
                return total_score

            current_instruction = (new_idx, parse_instruction(input[new_idx]))

        if (cycle - SIGNAL_STRENGTH_START) % SIGNAL_STRENGTH_LOOP == 0:
            total_score += signal_score * cycle

        current_instruction[1].tick()
        cycle += 1


def test():
    assert main(utils.file_handler.get_puzzle_input("10", filename="test")) == 13140


if __name__ == "__main__":
    test()
    print(main(utils.file_handler.get_puzzle_input("10")))
