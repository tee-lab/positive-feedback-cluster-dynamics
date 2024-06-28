from numpy import array, loadtxt, transpose, zeros
from os import path


def load_changes(file_path):
    data = transpose(loadtxt(file_path, dtype=int))
    changes, frequencies = data[0], data[1]
    length = len(changes)

    abs_changes_histogram = {}

    for i in range(length):
        change = changes[i]
        freq = frequencies[i]
        abs_change = abs(change)

        if abs_change in abs_changes_histogram:
            abs_changes_histogram[abs_change] += freq
        else:
            abs_changes_histogram[abs_change] = freq

    abs_freqs = []

    for key in sorted(abs_changes_histogram.keys()):
        abs_freqs.append(abs_changes_histogram[key])

    return array(abs_freqs, dtype=float)


# if __name__ == '__main__':
#     output = load_changes("C://Code//Github//vegetation-dynamics//results/tricritical/q0/100x100_residue/0p616/0p616_changes.txt")
#     print(output)
