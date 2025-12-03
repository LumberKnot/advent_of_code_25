from utils.file import get_input_list
import numpy as np

PATH = "inputs/dec3.txt"


def get_joltage_basic(battery: list[int]):
    np_bat = np.array(battery)
    idx_first = np.argmax(np_bat[:-1])

    idx_second = np.argmax(np_bat[idx_first + 1 :]) + idx_first + 1

    out = np_bat[idx_first] * 10 + np_bat[idx_second]

    return out


def get_joltage_big(battery: list[int], n_bat=12):
    bat = np.array(battery)

    scale = np.flip(np.asarray(10 ** np.arange(0, n_bat)))

    N = len(bat)
    start_idx = 0
    out = []

    for i in range(n_bat):
        stop_idx = N - n_bat + i + 1
        local_idx = np.argmax(bat[start_idx:stop_idx])
        """ 
        print(
            f"{i}: {stop_idx}: {bat[start_idx:stop_idx]} {bat[stop_idx :]} found {local_idx}"
        )
         """
        out.append(bat[start_idx + local_idx])
        start_idx += local_idx + 1

    out = np.asarray(out)
    return np.sum(scale * out)


input_raw = [
    "987654321111111",
    "811111111111119",
    "234234234234278",
    "818181911112111",
]

input_raw = get_input_list(PATH)
input = []
for line in input_raw:
    input.append([int(c) for c in line])

sum = 0
for line in input:
    sum += get_joltage_big(line)


print(sum)
