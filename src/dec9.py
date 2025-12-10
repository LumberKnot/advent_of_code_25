from utils.file import get_input_list
from tqdm import tqdm
import numpy as np
from sympy import Point, Segment


PATH = "inputs/dec9.txt"


def get_area(x1, y1, x2, y2):
    xdiff = abs(x1 - x2) + 1
    ydiff = abs(y1 - y2) + 1

    return xdiff * ydiff


def largest_area(points):
    N = len(points)

    largest_area = 0

    for first_index in tqdm(range(N - 1)):
        for second_index in range(first_index + 1, N):
            area = get_area(
                points[first_index][0],
                points[first_index][1],
                points[second_index][0],
                points[second_index][1],
            )
            if area > largest_area:
                largest_area = area

    return largest_area


def create_lines(points: np.ndarray):

    N = points.shape[0]

    lines = []

    for start in range(N):
        end = (start + 1) % N
        diff = points[start] - points[end]
        assert diff[0] == 0 or diff[1] == 0

        p1 = Point(points[start])
        p2 = Point(points[end])

        lines.append(Segment(p1, p2))

    return lines


def allowed(x1, y1, x2, y2, lines):
    """four lines make up a rectangle
    1. (x1,y1)-(x1,y2)
    2. (x1,y1)-(x2,y1)
    3. (x1,y2)-(x2,y2)
    4. (x2,y1)-(x2,y2)
    """

    segments = [
        Segment((x1, y1), (x1, y2)),
        Segment((x1, y1), (x2, y1)),
        Segment((x1, y2), (x2, y2)),
        Segment((x2, y1), (x2, y2)),
    ]

    for seg in segments:
        for line in lines:
            if len(seg.intersection(line)) == 1:
                # Exactly one intersection mean cross i.e not ok
                print(f"{x1},{y1}, {x2},{y2}")
                print(f"Intersect {seg} {line}")
                return False
    return True


def largest_allowed_area(points):

    points = np.array(points)
    N = points.shape[0]
    lines = create_lines(points)

    """New Idea!
    Save lines, see if crosses any line. 
        If so it is guaranteed to be unallowed
        Else it is guarenteed to be inside? (No proof atm)
    """

    largest_area = 0

    for first_index in range(N - 1):
        for second_index in range(first_index + 1, N):
            area = get_area(
                points[first_index][0],
                points[first_index][1],
                points[second_index][0],
                points[second_index][1],
            )
            if area > largest_area and allowed(
                points[first_index][0],
                points[first_index][1],
                points[second_index][0],
                points[second_index][1],
                lines,
            ):
                largest_area = area

    return largest_area


points = [
    [7, 1],
    [11, 1],
    [11, 7],
    [9, 7],
    [9, 5],
    [2, 5],
    [2, 3],
    [7, 3],
]

# points = [[int(i) for i in p.split(",")] for p in get_input_list(PATH)]
# print(largest_area(points)) # first star
print(largest_allowed_area(points))
