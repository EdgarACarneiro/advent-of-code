import utils.file_handler
import enum

class Choice(enum.Enum):
    ROCK = "A"
    PAPER = "B"
    SCISSORS  = "C"

class Result(enum.Enum):
    LOSS = "X"
    DRAW = "Y"
    WIN  = "Z"

CHOICE_POINTS = {
    Choice.ROCK: 1,
    Choice.PAPER: 2,
    Choice.SCISSORS: 3
}

RESULT_POINTS = {
    Result.LOSS: 0,
    Result.DRAW: 3,
    Result.WIN: 6
}

POSSIBLE_OUTCOMES = {
    Choice.ROCK: {
        Choice.ROCK: Result.DRAW,
        Choice.PAPER: Result.WIN,
        Choice.SCISSORS: Result.LOSS
    },
    Choice.PAPER: {
        Choice.ROCK: Result.LOSS,
        Choice.PAPER: Result.DRAW,
        Choice.SCISSORS: Result.WIN
    },
    Choice.SCISSORS: {
        Choice.ROCK: Result.WIN,
        Choice.PAPER: Result.LOSS,
        Choice.SCISSORS: Result.DRAW
    }
}

def get_result(line: str):
    enemy_choice, desired_res = line.split(" ")
    desired_res = Result(desired_res)

    # Out of lazyness, I'm not swapping the structure of the POSSIBLE_OUTCOMES
    # hashmap :sweat_smile:
    # Hence, this loop is becoming more inefficient then needed
    for choice, res in POSSIBLE_OUTCOMES.get(Choice(enemy_choice)).items():
        if res == desired_res:
            return RESULT_POINTS.get(desired_res) + CHOICE_POINTS.get(Choice(choice))

    raise RuntimeError(f"Unknown input line was given {line}")

def main(input: list[str]) -> str:
    return sum(
        get_result(line.strip()) for line in input if len(line.strip())
    )

def test():
    test_input ="""A Y
B X
C Z
"""
    assert main(test_input.split("\n")) == 12

if __name__ == "__main__":
    test()
    print(main(utils.file_handler.get_puzzle_input("02"))) # 11618