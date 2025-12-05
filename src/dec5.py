from utils.file import get_input_list
from tqdm import tqdm

PATH = "inputs/dec5.txt"

input = ["3-5", "10-14", "11-13", "16-20", "12-18", "", "1", "5", "8", "11", "17", "32"]

input = get_input_list(PATH)

break_point = input.index("")

ranges = [(int(r[0]), int(r[1])) for r in [r.split("-") for r in input[:break_point]]]
ingredients = [int(ing) for ing in input[break_point + 1 :]]


def one(ranges, ingredients):
    fine = []

    for ing in ingredients:
        for start, end in ranges:
            if start <= ing and ing <= end:
                # Fine
                fine.append(ing)
                break

    return len(fine)


def join_ranges(ranges):
    ranges = sorted(ranges, key=lambda x: (x[0], -x[1]))

    out = []

    cur_start, cur_end = ranges[0]

    for test_start, test_end in ranges[1:]:

        assert cur_start <= test_start

        if test_start <= cur_end:
            # Cojunt update current range
            cur_end = max(cur_end, test_end)

        else:
            # Very important, here you add the ranges
            out.append((cur_start, cur_end))

            # And update the inner range
            cur_start, cur_end = test_start, test_end

    # check wether final has entered

    last_in_start, last_in_end = out.pop()

    if cur_start <= last_in_end:
        # cojunt
        out.append((last_in_start, max(last_in_end, cur_end)))
    else:
        out = out + [(last_in_start, last_in_end), (cur_start, cur_end)]

    return out


def two(ranges):
    print(len(ranges))

    ranges = join_ranges(ranges)

    print(len(ranges))

    # Now we have a set of entierly disjunt ranges

    num_ranges = [end - start + 1 for start, end in ranges]
    print((ranges))
    print(num_ranges)
    print(sum(num_ranges))


two(ranges)
