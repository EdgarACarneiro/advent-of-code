import os

UTILS_DIR = os.path.dirname(os.path.abspath(__file__))

PROBLEM_INPUT_FORMATTER = "../day{day}/input_{problem}.txt"

def get_problem_input(day: str, problem: str, debug=False) -> list[str]:
    """
    Basic function to get the problem input of a given day and problem (1 or 2).
    Also allows for a debug mode that provides detailed logging info.
    Returns the file contents as the list of line (strs).
    """
    input_file = PROBLEM_INPUT_FORMATTER.format(day=day, problem=problem)

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