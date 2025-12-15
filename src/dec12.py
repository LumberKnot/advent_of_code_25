from utils.file import get_input_list
import numpy as np

# PATH_SHAPES = "inputs/dec12shape.txt"
PATH_REGIONS = "inputs/dec12target.txt"

""" Shapes
 0    1    2    3    4    5
##.  ###  #..  ###  ###  #.#
.##  .#.  ##.  ##.  ###  #.#
..#  ###  ###  .##  #..  ###
"""

shapes = {
    0: np.array([[1, 1, 0], [0, 1, 1], [0, 0, 1]], dtype=np.bool),
    1: np.array([[1, 1, 1], [0, 1, 0], [1, 1, 1]], dtype=np.bool),
    2: np.array([[1, 0, 0], [1, 1, 0], [1, 1, 1]], dtype=np.bool),
    3: np.array([[1, 1, 1], [1, 1, 0], [0, 1, 1]], dtype=np.bool),
    4: np.array([[1, 1, 1], [1, 1, 1], [1, 0, 0]], dtype=np.bool),
    5: np.array([[1, 0, 1], [1, 0, 1], [1, 1, 1]], dtype=np.bool),
}


def display_shape(shape: np.ndarray):
    for row in shape:
        row_str = ""
        for c in row:
            if c:
                row_str += "#"
            else:
                row_str += "."
        print(row_str)


def parse_regions(input):
    regions = []

    for line in input:
        dic = {}
        sides = (int(line[0:2]), int(line[3:5]))
        dic["sides"] = sides
        dic["area"] = sides[0] * sides[1]
        dic["shapes"] = [int(i) for i in line[7:].split(" ")]
        regions.append(dic)

    return regions


input = get_input_list(PATH_REGIONS)
regions = parse_regions(input)


# Running some quick sanity tests

shapes_vec = np.array(
    [
        shapes[0],
        shapes[1],
        shapes[2],
        shapes[3],
        shapes[4],
        shapes[5],
    ]
)

over, eq, under = 0, 0, 0  # Total area of shapes is over/equal/under that of the region
diff = []

for region in regions:
    # Test some values
    req = np.array(region["shapes"]).reshape((6, 1, 1))
    area_used = np.sum(req * shapes_vec)
    area = region["area"]
    # print(f"{area_used}/{area}")

    if area == area_used:
        eq += 1
    elif area_used > area:
        over += 1
    else:
        under += 1
        diff.append(area - area_used)


print("-" * 15)
print("u/e/o")
print(f"{under}/{eq}/{over}")
print("-" * 15)
print(np.mean(diff), np.max(diff), np.min(diff))
