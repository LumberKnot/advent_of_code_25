from utils.file import get_input_list

PATH = "inputs/dec4.txt"

input = [
    "..@@.@@@@.",
    "@@@.@.@.@@",
    "@@@@@.@.@@",
    "@.@@@@..@.",
    "@@.@@@@.@@",
    ".@@@@@@@.@",
    ".@.@.@.@@@",
    "@.@@@.@@@@",
    ".@@@@@@@@.",
    "@.@.@@@.@.",
]


def get_neigbors(x, y, size):
    possible = [(1, 0), (1, 1), (-1, 0), (-1, -1), (1, -1), (-1, 1), (0, 1), (0, -1)]
    neig = []
    for dy, dx in possible:
        nx = x + dx
        ny = y + dy

        if nx >= 0 and nx < size and ny >= 0 and ny < size:
            neig.append((nx, ny))
    return neig


def step(input):
    indices = []
    h, w = len(input), len(input[0])

    for y in range(h):
        for x in range(w):

            if input[y][x] == "@":
                # is paper
                neig = get_neigbors(x, y, h)
                neig = [input[y][x] for x, y in neig]
                if neig.count("@") < 4:
                    indices.append((x, y))

    return indices


input = get_input_list(PATH)

total = 0
while True:
    roll_idx = step(input)
    if len(roll_idx) == 0:
        break
    total += len(roll_idx)

    for x, y in roll_idx:
        input[y] = input[y][:x] + "." + input[y][x + 1 :]

print(total)
