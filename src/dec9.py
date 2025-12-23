from utils.file import get_input_list
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt


PATH = "inputs/dec9.txt"

""" What is a segment?

Interpreation one:
    2 points, 4 values

Interpreation two:
    type, level, ends, 4 values
    I.E horizontal, 5 (y=5), start, end
    type can be stored not per segment but as two lists

Should allow quick comparisons, especialy if the ends are sorted

Fingers crossed

"""


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


def intersects_any(test_segment, segments: np.ndarray):
    """
    Input should be a line and a set of lines
        where the type(vertical/horizontal) should be different
        between line and lines but same within lines

    for every segment in segments:
        if level is between test_segment changing dimension
            AND
        test_segment's level is between segments dimensions
    """

    (x1, y1), (x2, y2) = test_segment
    if x1 == x2:  # Verical line
        level = x1
        start = min(y1, y2)
        end = max(y1, y2)

    elif y1 == y2:  # Horizontal line
        level = y1
        start = min(x1, x2)
        end = max(x1, x2)

    else:
        raise ValueError("Not a straight line")

    # Level of other segments between correct span
    t1 = (segments[:, 0] > start) & (segments[:, 0] < end)

    # Level of this segment between other segments min/max
    t2 = (segments[:, 1] < level) & (segments[:, 2] > level)

    tot = t1 & t2

    return np.any(tot)


def create_lines(points: np.ndarray):

    N = points.shape[0]

    vertical, horizontal = [], []

    for start_idx in range(N):
        start = points[start_idx]
        end = points[(start_idx + 1) % N]
        diff = start - end
        assert diff[0] == 0 or diff[1] == 0

        if diff[0] == 0:  # Vertical line
            # level, end-min, end-max
            vertical.append([start[0], min(start[1], end[1]), max(start[1], end[1])])

        else:  # Horizontal line
            # level, end-min, end-max
            horizontal.append([start[1], min(start[0], end[0]), max(start[0], end[0])])

    return np.array(vertical), np.array(horizontal)


def allowed(x1, y1, x2, y2, horizontal, vertical):
    """four lines make up a rectangle
    1. (x1,y1)-(x1,y2)
    2. (x1,y1)-(x2,y1)
    3. (x1,y2)-(x2,y2)
    4. (x2,y1)-(x2,y2)
    """

    rect_horizontal = [
        ((x1, y1), (x2, y1)),
        ((x1, y2), (x2, y2)),
    ]

    rect_vertical = [
        ((x1, y1), (x1, y2)),
        ((x2, y1), (x2, y2)),
    ]

    for our_seg in rect_horizontal:
        if intersects_any(our_seg, vertical):
            return False
    for our_seg in rect_vertical:
        if intersects_any(our_seg, horizontal):
            return False

    return True


# ------- reduced area solution -------


def get_reduced_set(points):

    xs = set()
    ys = set()

    for p in points:
        xs.add(p[0])
        ys.add(p[1])

    xs = sorted(list(xs))
    ys = sorted(list(ys))

    org2new = {"x": {}, "y": {}}
    new2org = {"x": {}, "y": {}}

    for i, x in enumerate(xs):
        org2new["x"][x] = i + 1
        new2org["x"][i + 1] = x

    for i, y in enumerate(ys):
        org2new["y"][y] = i + 1
        new2org["y"][i + 1] = y

    return org2new, new2org


def convert(points, map):

    new_points = []

    for p in points:
        new_points.append([map["x"][p[0]], map["y"][p[1]]])

    return new_points


def create_tile_map(points: np.ndarray):

    N = points.shape[0]

    map_size = np.max(points, axis=0) + 2 * np.ones(2, dtype=int)

    line_map = np.zeros(map_size, dtype=np.bool)

    for start_idx in range(N):
        start = points[start_idx]
        end = points[(start_idx + 1) % N]

        startx, endx = min(start[0], end[0]), max(start[0], end[0])
        starty, endy = min(start[1], end[1]), max(start[1], end[1])

        if startx == endx:
            endx += 1
        elif starty == endy:
            endy += 1
        else:
            raise ValueError("Not a straigt line")

        line_map[startx:endx, starty:endy] = 1
        line_map[start[0], start[1]] = 1
        line_map[end[0], end[1]] = 1

    # Calculate what pixels belong to the background using breath first
    # We know (0,0) is allways in background from our reduce

    background = np.zeros(map_size, dtype=np.bool)
    background[0, 0] = 1
    queue = [(0, 0)]

    # 4 neigbours
    to_add = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while len(queue) > 0:
        src_point = queue.pop(0)  # The one we are woking from

        for diff in to_add:
            new_point = (src_point[0] + diff[0], src_point[1] + diff[1])

            # Check bounds
            if (
                new_point[0] < 0
                or new_point[0] >= map_size[0]
                or new_point[1] < 0
                or new_point[1] >= map_size[1]
            ):
                continue

            # Check maps
            if background[new_point] or line_map[new_point]:
                # Should not add
                continue

            background[new_point] = True
            queue.append(new_point)

    # Return inverse of background
    return np.invert(background)


def overlaps(c1, c2, tile_map):
    # Checks if rectangle from corner c1 - c2 overlaps ENTIERLY within the tilemap

    # Go from min_x, min_y to max_x,max_y

    minx, miny, maxx, maxy = (
        min(c1[0], c2[0]),
        min(c1[1], c2[1]),
        max(c1[0], c2[0]) + 1,
        max(c1[1], c2[1]) + 1,
    )

    rect = np.zeros(tile_map.shape, dtype=np.bool)

    rect[minx:maxx, miny:maxy] = 1
    overlap = rect & tile_map

    OVERLAPS = np.sum(rect) == np.sum(overlap)

    return OVERLAPS, rect


def largest_allowed_area(points):

    points = np.array(points)
    N = points.shape[0]

    largest_area = 0
    best_rect = None

    org2new, new2org = get_reduced_set(points)
    reduced_points = convert(points, org2new)

    # tile_large = create_tile_map(np.array(points))
    tile_small = create_tile_map(np.array(reduced_points))

    for first_index in range(N - 1):
        for second_index in range(first_index + 1, N):
            x1, y1, x2, y2 = (
                points[first_index][0],
                points[first_index][1],
                points[second_index][0],
                points[second_index][1],
            )
            area = get_area(x1, y1, x2, y2)
            if area > largest_area:
                over, rect = overlaps(
                    reduced_points[first_index],
                    reduced_points[second_index],
                    tile_small,
                )
                if over:
                    largest_area = area
                    best_rect = rect

    # I just want the display
    plt.imshow(best_rect + 3 * tile_small)
    plt.title(f"Best area {largest_area}")
    plt.show()

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


points = [[int(i) for i in p.split(",")] for p in get_input_list(PATH)]
# print(largest_area(points))  # first star

print(largest_allowed_area(points))  # Second star
