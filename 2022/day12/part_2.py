import utils.file_handler
import queue
from collections.abc import Callable


def a_star_search(
    starts: list[tuple[int, int]],
    goal: tuple[int, int],
    get_neighbors: Callable[[tuple[int, int]], list[tuple[int, int]]],
    heuristic: Callable[[tuple[int, int]], int],
):
    q = queue.PriorityQueue()
    came_from: dict[tuple[int, int], tuple[int, int] | None] = {}
    cost_so_far: dict[tuple[int, int], int] = {}

    for start in starts:
        q.put((heuristic(start), start))
        came_from[start] = None
        cost_so_far[start] = 0

    while not q.empty():
        current: tuple[int, int] = q.get()[1]

        if current == goal:
            break

        for next in get_neighbors(current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(current)
                q.put((priority, next))
                came_from[next] = current

    return came_from, cost_so_far


def heuristic(coords: tuple[int, int], goal: tuple[int, int]) -> int:
    return abs(goal[0] - coords[0]) + abs(goal[1] - coords[1])


def get_neighbors(
    coords: tuple[int, int], matrix: list[list[int]]
) -> list[tuple[int, int]]:
    current_val = matrix[coords[0]][coords[1]]
    neighbors = []

    # Top neighbor
    if coords[0] > 0 and matrix[coords[0] - 1][coords[1]] <= current_val + 1:
        neighbors.append((coords[0] - 1, coords[1]))

    # Bottom neighbor
    if (
        coords[0] < len(matrix) - 1
        and matrix[coords[0] + 1][coords[1]] <= current_val + 1
    ):
        neighbors.append((coords[0] + 1, coords[1]))

    # Left neighbor
    if coords[1] > 0 and matrix[coords[0]][coords[1] - 1] <= current_val + 1:
        neighbors.append((coords[0], coords[1] - 1))

    # Right neighbor
    if (
        coords[1] < len(matrix[0]) - 1
        and matrix[coords[0]][coords[1] + 1] <= current_val + 1
    ):
        neighbors.append((coords[0], coords[1] + 1))

    return neighbors


def main(input: list[str]) -> int:
    matrix: list[list[int]] = []
    starts: list[tuple[int, int]] = []
    goal: tuple[int, int] = (-1, -1)

    for i in range(len(input)):
        row = []
        for j in range(len(input[i].strip())):
            if input[i][j] == "a":
                starts.append((i, j))

            elif input[i][j] == "E":
                goal = (i, j)
                row.append(ord("z"))
                continue

            row.append(ord(input[i][j]))
        matrix.append(row)

    heuristic_fn = lambda coords: heuristic(coords, goal)
    get_neighbors_fn = lambda coords: get_neighbors(coords, matrix)

    _, path_costs = a_star_search(starts, goal, get_neighbors_fn, heuristic_fn)

    return path_costs[goal]


def test():
    assert (
        main(
            """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""".split(
                "\n"
            )
        )
        == 29
    )


if __name__ == "__main__":
    test()
    print(main(utils.file_handler.get_puzzle_input("12")))
