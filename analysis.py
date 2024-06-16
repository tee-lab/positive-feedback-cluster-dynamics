from numpy import array, loadtxt, zeros
from pickle import dump

from utils import *


def cluster_size_distribution(landscapes, file_root):
    size = landscapes[0].shape[0]
    clusters_histogram = zeros(size * size, dtype=int)
    for landscape in landscapes:
        clusters_histogram += get_csd(landscape)[1:]
    clusters_histogram = right_trim(clusters_histogram)
    
    output_string = ""
    for i in range(len(clusters_histogram)):
        output_string += f"{i + 1} {clusters_histogram[i]}\n"

    fp = open("outputs/" + file_root + "csd.txt", "w")
    fp.write(output_string)
    fp.close()

    fp = open("outputs/" + file_root + "lattices.pkl", "wb")
    dump(landscapes, fp)
    fp.close()


def cluster_dynamics(clusters_before, clusters_after, size, file_root):
    length = len(clusters_before)
    changes_histogram = {}
    for i in range(-size * size, size * size):
        changes_histogram[i] = 0

    for i in range(length):
        prominent_cluster_before = max(clusters_before[i])
        prominent_cluster_after = max(clusters_after[i])
        change = prominent_cluster_after - prominent_cluster_before
        changes_histogram[change] += 1

    for i in range(-size * size, size * size):
        if changes_histogram[i] == 0:
            del changes_histogram[i]
        else:
            break

    for i in range(size * size - 1, -size * size, -1):
        if changes_histogram[i] == 0:
            del changes_histogram[i]
        else:
            break

    output_string = ""
    for key in changes_histogram.keys():
        output_string += f"{key} {changes_histogram[key]}\n"

    fp = open("outputs/" + file_root + "cd.txt", "w")
    fp.write(output_string)
    fp.close()
    

def analysis(simulation_name, num_simulations, parameters):
    clusters_before = []
    clusters_after = []
    landscapes = []

    if simulation_name == "tdp":
        p = parameters[0]
        q = parameters[1]
        file_root = f"tdp_{str(p).replace('.', 'p')}_{str(q).replace('.', 'q')}_"

    for i in range(num_simulations):
        file_name = f"temp/{file_root}{i}_landscape.txt"
        landscape = loadtxt(file_name, dtype=bool)
        landscapes.append(landscape)

        file_name = f"temp/{file_root}{i}_dynamics.txt"
        raw_data = open(file_name, "r").read()
        lines = raw_data.split("\n")

        for line in lines[:-1]:
            line_split = line.split(":")
            clusters_before.append(list(map(int, line_split[0].split())))
            clusters_after.append(list(map(int, line_split[1].split())))

    cluster_size_distribution(landscapes, file_root)
    cluster_dynamics(clusters_before, clusters_after, landscape.shape[0], file_root)


if __name__ == '__main__':
    simulation_name = "tdp"
    num_simulations = 4
    parameters = [0.7, 0]

    analysis(simulation_name, num_simulations, parameters)