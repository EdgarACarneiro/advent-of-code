import utils.file_handler

UNIQUE_CHARS_GOAL = 4


def main(input: list[str]) -> int:
    sw_begin = 0
    sw_end = 1
    input_str = input[0]

    while sw_end + 1 <= len(input_str):
        if input_str[sw_end] in input_str[sw_begin:sw_end]:
            sw_begin += 1
            continue
        else:
            sw_end += 1
            if sw_end - sw_begin >= UNIQUE_CHARS_GOAL:
                return sw_end

    raise Exception(f"There is no start-of-packet marker in {input_str}")


def test():
    assert main("""mjqjpqmgbljsphdztnvjfqwrcgsmlb""".split("\n")) == 7
    assert main("""bvwbjplbgvbhsrlpgdmjqwftvncz""".split("\n")) == 5
    assert main("""nppdvjthqldpwncqszvftbrmjlhg""".split("\n")) == 6
    assert main("""nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg""".split("\n")) == 10
    assert main("""zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw""".split("\n")) == 11


if __name__ == "__main__":
    test()
    print(main(utils.file_handler.get_puzzle_input("06")))
