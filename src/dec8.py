from utils.file import get_input_list
import numpy as np

PATH = "inputs/dec8.txt"

input, conections = [
    "162,817,812",
    "57,618,57",
    "906,360,560",
    "592,479,940",
    "352,342,300",
    "466,668,158",
    "542,29,236",
    "431,825,988",
    "739,650,466",
    "52,470,668",
    "216,146,977",  # 10
    "819,987,18",
    "117,168,530",  # 12
    "805,96,715",
    "346,949,466",
    "970,615,88",
    "941,993,340",
    "862,61,35",
    "984,92,344",
    "425,690,689",
], 10

input, conections = get_input_list(PATH), 1000


def find_circuits(points: np.ndarray, conections):

    N = points.shape[0]

    circuits = [0] * N
    next_circuit_id = 1
    made_conections = 0

    """  A matrix wiht values from index to index
        First dimension is from index
        Should not matter as they are symetrical
     """
    distances = np.zeros((N, N))

    for from_idx in range(N):
        temp = np.sum((points[from_idx] - points) ** 2, axis=1)
        distances[from_idx] = temp

    pair_distances = []

    for i in range(N - 1):
        for j in range(i + 1, N):
            pair_distances.append((i, j, distances[i, j]))

    pair_distances = sorted(pair_distances, key=lambda x: x[2])

    for i, j, _ in pair_distances:
        # Algo time, we know we are curently holding the shortest non handeled case

        made_conections += 1
        if circuits[i] == 0 and circuits[j] == 0:
            # None have been given a circuit
            circuits[i] = next_circuit_id
            circuits[j] = next_circuit_id
            next_circuit_id += 1
            # print(f"Joining {i:2>}-{j:2<}")

        elif circuits[i] == 0:
            # J was already assigned
            circuits[i] = circuits[j]
            # made_conections += 1
            # print(f"Adding {i:2>}-{j:2<}")

        elif circuits[j] == 0:
            # I was already assigned
            circuits[j] = circuits[i]
            # made_conections += 1
            # print(f"Adding {i:2>}-{j:2<}")

        # Else both where assigned
        else:
            print(
                f"circuit id {circuits[i]} tried to join with id {circuits[j]} LETTING THEM"
            )
            out = circuits[j]
            for e in range(N):
                if circuits[e] == out:
                    circuits[e] = circuits[i]

        if made_conections == conections:
            break

    print(f"Len circ: {len(circuits)} next: {next_circuit_id}")
    print(circuits)

    counts = {}
    loners = 0

    for c in circuits:
        if c != 0:
            counts[c] = counts.get(c, 0) + 1
        else:
            loners += 1

    print(counts, loners)

    return np.prod((sorted(counts.values(), reverse=True))[0:3])


def close_loop(points):

    N = points.shape[0]

    circuits = [0] * N
    next_circuit_id = 1

    """  A matrix wiht values from index to index
        First dimension is from index
        Should not matter as they are symetrical
     """
    distances = np.zeros((N, N))

    for from_idx in range(N):
        temp = np.sum((points[from_idx] - points) ** 2, axis=1)
        distances[from_idx] = temp

    pair_distances = []

    for i in range(N - 1):
        for j in range(i + 1, N):
            pair_distances.append((i, j, distances[i, j]))

    pair_distances = sorted(pair_distances, key=lambda x: x[2])

    """ Theory:
        we do not need to simulte any of the conections,
        as we know in the end the ones at index N have to be the final conetion
        
        In the begining we have N independent circuits
        Every conection, be a new circ, joining a circ or
        joining two circutis reduces the number of circuits by 1 

        Nope, things might and often will be in the same pair
    """

    num_circuits = N

    for i, j, _ in pair_distances:

        """The 5 cases to be handeled and a check in the end"""

        if circuits[i] == circuits[j] and circuits[i] != 0:
            # They already belong to the same circuit
            continue

        num_circuits -= 1
        if circuits[i] == 0 and circuits[j] == 0:
            # None have been given a circuit
            circuits[i] = next_circuit_id
            circuits[j] = next_circuit_id
            next_circuit_id += 1

        elif circuits[i] == 0:
            # J was already assigned
            circuits[i] = circuits[j]

        elif circuits[j] == 0:
            # I was already assigned
            circuits[j] = circuits[i]

        # Else both where assigned
        else:
            out = circuits[j]
            for e in range(N):
                if circuits[e] == out:
                    circuits[e] = circuits[i]

        if num_circuits == 1:
            print(f"Winners are {i}{j}")
            print(points[i])
            print(points[j])
            return points[i, 0] * points[j, 0]


def format_input(input):
    out = np.array([[int(n) for n in line.split(",")] for line in input])
    return out


points = format_input(input)
# print(find_circuits(points, conections)) #first star
print(close_loop(points))  # second star
