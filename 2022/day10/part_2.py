import utils.file_handler
import abc

CRT_LOOP = 40


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


def get_sprite_positions(idx: int):
    return (idx - 1, idx, idx + 1)


def main(input: list[str]) -> list[str]:

    res: list[str] = []
    crt_row: str = ""
    signal_score: int = 1
    cycle: int = 0
    current_idx: int = 0
    current_instruction: Instruction = parse_instruction(input[0])

    while True:
        # Process next instruction if current one has finished
        if current_instruction.has_finished():
            # Process finished instruction
            signal_score += current_instruction.get_value()

            current_idx += +1
            # We processed all instructions and there isn't any instruction
            # being processed
            if current_idx >= len(input):
                # Append the current crt_row
                res.append(crt_row)
                return res

            current_instruction = parse_instruction(input[current_idx])

        if cycle % CRT_LOOP == 0:
            res.append(crt_row)
            crt_row = ""

        # Update the CRT row
        crt_row += (
            "█" if (cycle % CRT_LOOP) in get_sprite_positions(signal_score) else " "
        )

        current_instruction.tick()
        cycle += 1


def test():
    assert "".join(
        main(utils.file_handler.get_puzzle_input("10", filename="test"))
    ) == "".join(
        [
            "██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ",
            "███   ███   ███   ███   ███   ███   ███ ",
            "████    ████    ████    ████    ████    ",
            "█████     █████     █████     █████     ",
            "██████      ██████      ██████      ████",
            "███████       ███████       ███████     ",
        ]
    )


if __name__ == "__main__":
    test()
    for row in main(utils.file_handler.get_puzzle_input("10")):
        print(row)
