from utils.file import get_input_list

PATH = "inputs/dec11.txt"

""" Insights for part 2

- No cycles
- Part 1 required only nodes single visit, dirived from no cycles

"""

# Utils -----


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


# Never used, had an idea of the input data
def invert_graph(org_graph):

    new_graph = {}

    for end, starts in org_graph.items():
        for start in starts:
            new_graph[start] = new_graph.get(start, [])
            new_graph[start].append(end)

    return new_graph


# Used for sanity check
def has_cycle(graph, node, visited, rec_stack):
    """Debug function to test if it has a cycle in it"""

    if node in rec_stack:
        print(f"Node {node} found in {rec_stack}")
        return True

    if node in visited:
        return False

    nexts = graph.get(node, [])

    visited.add(node)
    rec_stack.add(node)

    for next in nexts:
        if has_cycle(graph, next, visited, rec_stack):
            return True

    rec_stack.remove(node)
    return False


def topological_sort(graph):
    """

    Sorts all nodes in topological order

    Using Khan's algorithm as described in wikipedia
    """

    L = []  # ordered list of nodes in topological order
    i_graph = invert_graph(graph)
    S = graph.keys() - i_graph.keys()  # Set of all nodes with no incoming edges
    visited = set()  # All nodes processed

    while len(S) > 0:
        n = S.pop()
        visited.add(n)
        L.append(n)

        others = graph.get(n, [])  # Nodes that connect to

        for m in others:
            starts = set(i_graph[m])  # Other nodes that connect to m
            if starts & visited == starts:  # If all previous nodes have been vissited
                S.add(m)

    return L


# Solution ----


# One star
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


# Naive two star
def find_num_allowed_paths(graph, traversed: set, current, reqired, target="out"):
    """Question is a bit unclear but my theory is

    Nodes - can be traversed once (Try out)
    Edges - can only be traversed once!

    Solve with depth first

    Termination conditions
        Reached target - return 1 if all required have been traversed
        No nodes to traverse - return 0

    """

    if current == target:
        # Since we know required does not overlap with "out" we can:
        nodes = {s for s in traversed}
        # if (nodes & reqired) == reqired:
        return 1
        return 0

    paths = 0

    for next in graph.get(current, []):
        if next not in traversed:  # not yet traversed node
            traversed.add(next)
            paths += find_num_allowed_paths(graph, traversed, next, reqired, target)
            traversed.remove(next)

    return paths


def paths(graph, start, end, top_sorted):
    """Using BFS

    Time:  O(E)
    Space: O(No clue)

    odes - can be traversed several times
    Edges - can only be traversed once

    """
    paths = {start: 1}

    visited = set()
    belong = set()  # belong (s) to a possible path
    belong.add(start)

    for node in top_sorted:
        if not node in belong:
            continue
        next_nodes = graph.get(node, [])
        for next in next_nodes:
            belong.add(next)
            # print(f"Processing {node}->{next}")
            paths[next] = paths.get(next, 0) + paths[node]
            if (node, next) not in visited:
                visited.add((node, next))

    # print(paths)

    return paths.get(end, 0)


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

# Test for sanity
input = [
    "svr: aaa fft bbb",
    "aaa: fft",
    "bbb: fft",
    "fft: dac",
    "dac: ccc out",
    "ccc: out",
    "you: out",
]

input = get_input_list(PATH)
graph = build_graph(input)
top_sorted = topological_sort(graph)


# too low 368406
# too low 1693976470344


# print(find_num_paths(graph, set(), "you", "out"))  # First star
# print(find_num_allowed_paths(graph, set(), "fft", {}, "dac"))  # Second star

p11 = paths(graph, "svr", "dac", top_sorted)
p12 = paths(graph, "dac", "fft", top_sorted)
p13 = paths(graph, "fft", "out", top_sorted)

p21 = paths(graph, "svr", "fft", top_sorted)
p22 = paths(graph, "fft", "dac", top_sorted)
p23 = paths(graph, "dac", "out", top_sorted)


print(p11, p12, p13)
print(p21, p22, p23)

print(p11 * p12 * p13)
print(p21 * p22 * p23)
