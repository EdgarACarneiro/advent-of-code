import utils.file_handler

def main(input: list[str]) -> str:
    elfs_calories = [0]

    elf_num = 0
    for line in input:
        # New elf parsing
        if not len(line.strip()):
            elf_num += 1
            elfs_calories.append(0)
            continue

        # Otherwise, add calories to the current elf
        elfs_calories[elf_num] += int(line.strip())

    return max(elfs_calories)

def test():
    test_input ="""
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""
    assert main(test_input.split("\n")) == 24000

if __name__ == "__main__":
    test()
    print(main(utils.file_handler.get_puzzle_input("01"))) # 73211