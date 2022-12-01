import utils.file_handler

def get_sum_max_3(input: list[int]) -> int:
    """
    Get the sum of the maximum 3 values in the provided string list
    """
    max1 = 0
    max2 = 0
    max3 = 0

    for num in input:
        if num >= max1:
            max3 = max2
            max2 = max1
            max1 = num

        elif num >= max2:
            max3 = max2
            max2 = num

        elif num > max3:
            max3 = num

    return sum([max1, max2, max3])

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

    return get_sum_max_3(elfs_calories)

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
    assert main(test_input.split("\n")) == 45000

if __name__ == "__main__":
    test()
    print(main(utils.file_handler.get_problem_input("01", 2))) # 213958