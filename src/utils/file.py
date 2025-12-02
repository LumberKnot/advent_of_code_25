def get_input_list(path):
    with open(path, "r") as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        return lines


def get_input_string(path):
    with open(path, "r") as f:
        return f.read()
