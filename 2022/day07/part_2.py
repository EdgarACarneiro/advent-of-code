import utils.file_handler
import functools
import abc


DISK_SPACE = 70000000
UPDATE_UNUSED_SPACE_NEEDED = 30000000


class FileSystemElement(abc.ABC):
    name: str
    size: int

    def __init__(self, name: str):
        self.name = name

    @abc.abstractmethod
    def get_size(self) -> int:
        pass

    @abc.abstractmethod
    def get_delete_candidate(self, necessary_space: int):
        pass


class File(FileSystemElement):
    def __init__(self, name: str, size: int):
        super().__init__(name)
        self.size = int(size)

    def get_size(self) -> int:
        return self.size

    def get_delete_candidate(self, necessary_space: int):
        return None

    def __str__(self):
        return f"- {self.size} {self.name}\n"


class Dir(FileSystemElement):

    elements: list[FileSystemElement]

    def __init__(self, name: str):
        super().__init__(name)
        self.elements = []

    @functools.lru_cache
    def get_size(self) -> int:
        return sum(el.get_size() for el in self.elements)

    def get_delete_candidate(self, necessary_space: int):
        candidate = None

        for el in self.elements:
            possible_candidate = el.get_delete_candidate(necessary_space)
            if possible_candidate is not None:
                if (
                    candidate is None
                    or possible_candidate.get_size() < candidate.get_size()
                ):
                    candidate = possible_candidate

        if candidate is None:
            return self if self.get_size() >= necessary_space else None

        return candidate

    def add_element(self, element: FileSystemElement):
        self.elements.append(element)

    def get_child(self, name):
        for el in self.elements:
            if el.name == name:
                return el

        raise Exception("Element not found")

    def __str__(self):
        res = "{Start dir " + self.name + " }\n"
        for el in self.elements:
            res += str(el)
        res += "{End dir " + self.name + " }\n"
        return res


class CommandLineParser:
    path: list[Dir]

    def __init__(self):
        self.path = [Dir("/")]

    def get_root(self):
        return self.path[0]

    def parse_cmd(self, cmd: str):
        cmd_parts = cmd.split(" ")

        if cmd_parts[0] != "$":
            # This is the result of a ls command
            # Parse current element
            if cmd_parts[0] == "dir":
                curr_element = Dir(cmd_parts[1])
            else:
                curr_element = File(cmd_parts[1], cmd_parts[0])

            # Add element to current dir
            self.path[-1].add_element(curr_element)

        else:
            # We can ignore ls commands, only cd matters with the current design
            # approach
            if cmd_parts[1] == "cd":
                if cmd_parts[2] == "/":
                    self.path = [self.get_root()]

                elif cmd_parts[2] == "..":
                    self.path = self.path[:-1]

                else:
                    self.path.append(self.path[-1].get_child(cmd_parts[2]))


def main(input: list[str]) -> int:
    parser = CommandLineParser()

    for cmd in input:
        parser.parse_cmd(cmd.strip())

    return (
        parser.get_root()
        .get_delete_candidate(
            UPDATE_UNUSED_SPACE_NEEDED - (DISK_SPACE - parser.get_root().get_size())
        )
        .get_size()
    )


def test():
    assert (
        main(
            """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""".split(
                "\n"
            )
        )
        == 24933642
    )


if __name__ == "__main__":
    test()
    print(main(utils.file_handler.get_puzzle_input("07")))
