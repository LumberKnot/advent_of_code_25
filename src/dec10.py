from utils.file import get_input_list
import regex as re
from tqdm import tqdm
import numpy as np


PATH = "inputs/dec10.txt"


def parse_machine(line: str):
    """Using regex

    pattern: [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}

    (0,3,4): ...... -> #..##.
        so we need to maintain ORDER the lights to be able to use index
            ..#.#. should be [0,0,1,0,1,0]
        we need to invert to use buttons as binary operations
            (0,3,4) should be (for a size of 5): 011001 <- 2^4 + 2^3 + 2^0
            ..#.#. should be: [0,0,1,0,1,0]:     010100

    """

    indicators_regex = re.compile(r"\[.*\]")
    buttons_regex = re.compile(r"\([\d,]*\)")
    joltage_regex = re.compile(r"{[\d,]*}")

    machine = {}

    # ----------------- indicators ---------------------------
    indicators_found = re.findall(indicators_regex, line)
    assert len(indicators_found) == 1  # Only one found
    indicators_string = indicators_found[0][1:-1]

    N = len(indicators_string)  # Super important value for all other convertions
    machine["N"] = N

    indicators = sum([2**i for i, c in enumerate(indicators_string) if c == "#"])
    machine["goal_string"] = indicators_string
    machine["goal"] = indicators

    # buttons
    buttons_found = re.findall(buttons_regex, line)
    assert len(buttons_found) > 0
    buttons_lists = [[int(i) for i in l[1:-1].split(",")] for l in buttons_found]
    machine["buttons"] = buttons_lists
    buttons_lists = [sum([2**i for i in list]) for list in buttons_lists]
    machine["buttons_int"] = buttons_lists

    # joltage
    joltage_found = re.findall(joltage_regex, line)
    assert len(joltage_found) == 1
    joltage = [int(i) for i in joltage_found[0][1:-1].split(",")]
    machine["joltage"] = joltage

    return machine


def solve_button_steps(machine):
    """
    Solving by breath first search. As soon as a solution is found we know it is optimal

    Adding into the queue is a dict/touple of shape
        current : int - What pattern we have reached so far
        steps : int   - How many steps it was solved in

    """

    queue = []

    queue.append((0, 0))

    while len(queue) > 0:

        current, steps = queue.pop(0)
        steps += 1  # Danger zone

        for button in machine["buttons_int"]:
            next = current ^ button
            if next == machine["goal"]:  # Done
                return steps
            queue.append((next, steps))

    # if we reached this something is whaky
    raise ValueError("Should not reach this point")


def solve_joltage(machine):
    """
    We have a set of linear equations!

    They should be solvable!!

    We always have a (n,m) matrix A
    We always have a (m,1) vector B of expected answers

    We seek to find x

    """

    # some pre-procesing i.e turning into workable np arrays

    goal_joltage = np.array(machine["joltage"], dtype=int)
    goal_joltage = goal_joltage[:, np.newaxis]

    buttons = []

    for but in machine["buttons"]:
        temp = np.zeros(machine["N"], dtype=int)
        temp[but] = 1
        buttons.append(temp)

    A = np.asarray(buttons).T  # Should be transform!

    print(np.linalg.matrix_rank(A))

    try:
        x = np.linalg.solve(A, goal_joltage)
        print("YES")
    except np.linalg.LinAlgError:
        print(f"NO")

    return

    rank = np.linalg.matrix_rank(A)

    print(
        f"{A.shape}: {rank:2>}/{A.shape[0]:2<} for square {goal_joltage.shape} {"FULL" if rank==A.shape[0] else ""}"
    )

    """A^-1 * b = x can use psudo inverse"""


input = [
    "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
    "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
    "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}",
]

# input = get_input_list(PATH)


for line in input:
    m = parse_machine(line)
    solve_joltage(m)
