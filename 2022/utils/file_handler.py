import os

UTILS_DIR = os.path.dirname(os.path.abspath(__file__))

PUZZLE_INPUT_FORMATTER = "../day{day}/{filename}.txt"


def get_puzzle_input(day: str, filename: str = "input", debug=False) -> list[str]:
    """
    Basic function to get the puzzle input of a given day and part (1 or 2).
    Also allows for a debug mode that provides detailed logging info.
    Returns the file contents as the list of line (strs).
    """
    input_file = PUZZLE_INPUT_FORMATTER.format(day=day, filename=filename)

    if debug:
        print(f"Opening file {input_file}")

    contents = []
    with open(os.path.join(UTILS_DIR, input_file)) as fp:
        if debug:
            print("File contents are:")

        for line in fp:
            if debug:
                print(line)

            contents.append(line)

    if debug:
        print(f"Finished reading {input_file}")

    return contents
