input_basic = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"


def get_input():
    with open("inputs/dec2.txt", "r") as f:
        return f.read()


def format_input(input: str):
    ranges = input.split(",")
    splits = [ran.split("-") for ran in ranges]
    return splits


def is_invalid(val: str) -> bool:

    N = len(val)

    if N == 0:
        raise ValueError("Id is very short")

    if N == 1:
        return False  # Lenght one will never contain repetitions

    """ 
    if N % 2 != 0:
        return False
    possible_splits = [int(N / 2)] 
    """

    possible_splits = [
        i for i in range(1, N) if N % i == 0
    ]  # I think this might be later

    for split in possible_splits:
        sub = [(val[i : i + split]) for i in range(0, N, split)]

        # Check if it was made by repetiotion
        if len(set(sub)) == 1:
            # Everything was equal
            return True

    return False


def find_invalid(ranges):
    invalids = []

    for start, end in ranges:
        # temp_inv = []
        start, end = int(start), int(end)

        for test in range(start, end + 1):
            test_str = str(test)
            if is_invalid(test_str):
                # temp_inv.append(test)
                invalids.append(test)
        # print(f"{start}-{end}: {temp_inv}")

    return sum(invalids)


# input = format_input(input_basic)
input = format_input(get_input())
print(find_invalid(input))
