from utils.file import get_input_list

PATH = "inputs/dec11.txt"


def build_graph(lines):

    graph = {}

    """ I'll use indeces for speed but should be implemented with regex
        0-2: start
        3, 4: ':', ' '
        5-> end(s)
    """

    for line in lines:
        start = line[0:3]
        ends = line[5:].split(" ")

        assert start not in graph.keys()  # Should never have the same twice

        graph[start] = ends

    return graph


def find_num_paths(graph, traversed: set, current, target="out"):
    """Question is a bit unclear but my theory is

    Nodes - can be traversed several times
    Edges - can only be traversed once!

    Solve with depth first

    Termination conditions
        Reached target - return 1
        No nodes to traverse - return 0

    """

    if current == target:
        return 1

    paths = 0

    for next in graph.get(current, []):
        if (current, next) not in traversed:  # not yet traversed edge
            traversed.add((current, next))
            paths += find_num_paths(graph, traversed, next, target)
            traversed.remove((current, next))

    return paths


def find_num_allowed_paths(graph, traversed: set, current, reqired, target="out"):
    """Question is a bit unclear but my theory is

    Nodes - can be traversed several times
    Edges - can only be traversed once!

    Solve with depth first

    Termination conditions
        Reached target - return 1 if all required have been traversed
        No nodes to traverse - return 0

    """

    if current == target:
        # Since we know required does not overlap with "out" we can:
        nodes = {s for s, _ in traversed}
        if (nodes & reqired) == reqired:
            return 1
        return 0

    paths = 0

    for next in graph.get(current, []):
        if (current, next) not in traversed:  # not yet traversed edge
            traversed.add((current, next))
            paths += find_num_allowed_paths(graph, traversed, next, reqired, target)
            traversed.remove((current, next))

    return paths


input = [  # Test input for first star
    "aaa: you hhh",
    "you: bbb ccc",
    "bbb: ddd eee",
    "ccc: ddd eee fff",
    "ddd: ggg",
    "eee: out",
    "fff: out",
    "ggg: out",
    "hhh: ccc fff iii",
    "iii: out",
]

input = [  # Test input for second star
    "svr: aaa bbb",
    "aaa: fft",
    "fft: ccc",
    "bbb: tty",
    "tty: ccc",
    "ccc: ddd eee",
    "ddd: hub",
    "hub: fff",
    "eee: dac",
    "dac: fff",
    "fff: ggg hhh",
    "ggg: out",
    "hhh: out",
]

input = get_input_list(PATH)
graph = build_graph(input)


# print(find_num_paths(graph, set(), "you", "out"))  # First star
# print(find_num_allowed_paths(graph, set(), "svr", {"dac", "fft"}))
