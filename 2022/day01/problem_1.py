import utils.file_handler

def main(input: list[str]) -> str:
    pass

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
    print(main(utils.file_handler.get_problem_input("01", 1)))