import utils.file_handler

CHOICE_POINTS = {
    "X": 1,
    "Y": 2,
    "Z": 3
}

RESULT_POINTS = {
    "A": {
        "X": 3,
        "Y": 6,
        "Z": 0
    },
    "B": {
        "X": 0,
        "Y": 3,
        "Z": 6
    },
    "C": {
        "X": 6,
        "Y": 0,
        "Z": 3
    }
}

def get_result(line: str):
    enemy_choice, own_choice = line.split(" ")

    return RESULT_POINTS.get(enemy_choice).get(own_choice) + CHOICE_POINTS.get(own_choice)

def main(input: list[str]) -> str:
    return sum(
        get_result(line.strip()) for line in input if len(line.strip())
    )

def test():
    test_input ="""A Y
B X
C Z
"""
    assert main(test_input.split("\n")) == 15

if __name__ == "__main__":
    test()
    print(main(utils.file_handler.get_puzzle_input("02"))) # 12772