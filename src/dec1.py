from utils.file import get_input_list


def password(seq, start=50):
    zero_cnt = 0
    zero_pass = 0
    dial = start

    print(f"Start: {dial}")

    for inst in seq:
        dir = 1 if inst[0] == "R" else -1
        size = int(inst[1:])

        laps = int(size / 100)
        zero_pass += laps
        size -= laps * 100

        new_dial = dial + (dir * size)

        if (new_dial < 0 or new_dial > 100) and dial != 0:
            # PASSED and did not stop on 0
            zero_pass += 1

        dial = new_dial % 100
        if dial == 0:
            zero_pass += 1
            zero_cnt += 1

    return zero_cnt, zero_pass


seq = get_input_list("inputs/dec1.txt")
# seq = ["L68", "L30", "R48", "L5", "R60", "L55", "L1", "L99", "R14", "L82"]
first, second = password(seq)
print(f"First star: {first}\nSecond star: {second}")
