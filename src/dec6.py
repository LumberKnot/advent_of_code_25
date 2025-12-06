from utils.file import get_input_list
import numpy as np

PATH = "inputs/dec6.txt"

input = ["123 328  51 64 ", " 45 64  387 23 ", "  6 98  215 314", "*   +   *   +"]

input = get_input_list(PATH)


def first(input):
    numbers = np.array([[int(n) for n in s.split()] for s in input[:-1]])
    ops = input[-1].split()

    sums = np.sum(numbers, axis=0)
    prods = np.prod(numbers, axis=0)

    assert len(prods) == len(sums)
    assert len(prods) == len(ops)

    totals = []

    for i, op in enumerate(ops):
        match op:
            case "+":
                totals.append(sums[i])

            case "*":
                totals.append(prods[i])

            case _:
                raise ValueError(f"Unexpecter op: {op}")

    return sum(totals)


def second(input):

    ops = input[-1]

    N = len(input[0])

    nums = input[:-1]

    data = ["".join([row[idx] for row in nums]).strip() for idx in range(N - 1, -1, -1)]

    numbers = []

    temp = []
    for p in data:
        if p == "":
            if len(temp) == 0:
                raise ValueError("Sum ting wrong")
            numbers.append(temp)
            temp = []
        else:
            temp.append(int(p))

    if len(temp) == 0:
        raise ValueError("Sum ting wrong")
    numbers.append(temp)

    inv_ops = list(reversed(ops.split()))

    totals = []

    for i, op in enumerate(inv_ops):
        match op:
            case "+":
                totals.append(np.sum(numbers[i]))

            case "*":
                totals.append(np.prod(numbers[i]))

            case _:
                raise ValueError(f"Unexpecter op: {op}")

    return sum(totals)


# print(first(input))
print(second(input))
