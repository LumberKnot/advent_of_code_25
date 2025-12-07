from utils.file import get_input_list

PATH = "inputs/dec7.txt"

""" Undestanding what a timeline would mean

..S..
..1.. - 2 Timelines
.1^2.
.1.2.

....S....
....1....
...1^2...
...1.2... - 4 Timelines as A represents both left,right and righ,left
..1^A^4.. - 4 timelines 3 splits
..1.A.4..

"""

map = [
    ".......S.......",
    "...............",
    ".......^.......",
    "...............",
    "......^.^......",
    "...............",
    ".....^.^.^.....",
    "...............",
    "....^.^...^....",
    "...............",
    "...^.^...^.^...",
    "...............",
    "..^...^.....^..",
    "...............",
    ".^.^.^.^.^...^.",
    "...............",
]

map = get_input_list(PATH)


def solver(map):

    n_rows = len(map)
    n_cols = len(map[0])

    # Find start
    beams = {map[0].index("S"): 1}

    assert len(beams) == 1
    assert -1 not in beams

    # Main part of the function

    spilts = 0

    for cur_row in range(1, n_rows):  # Skipp start row
        new_beams = {}

        for beam_col, timelines in beams.items():
            if map[cur_row][beam_col] == "^":
                spilts += 1
                # split
                left, right = beam_col - 1, beam_col + 1
                if left >= 0:
                    # within bounds
                    new_beams[left] = new_beams.get(left, 0) + timelines
                if right < n_cols:
                    # within bounds
                    new_beams[right] = new_beams.get(right, 0) + timelines
            else:
                new_beams[beam_col] = new_beams.get(beam_col, 0) + timelines

        beams = new_beams
        # print(beams)
    return spilts, sum(beams.values())


first, second = solver(map)
# print(first)
print(second)
