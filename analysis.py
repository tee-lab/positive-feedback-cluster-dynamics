from numpy import array, histogram, loadtxt, zeros
from pickle import dump
from tqdm import tqdm

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

    fp = open("outputs\\" + file_root + "csd.txt", "w")
    fp.write(output_string)
    fp.close()

    fp = open("outputs\\" + file_root + "lattices.pkl", "wb")
    dump(landscapes, fp)
    fp.close()


def cluster_dynamics(clusters_before, clusters_after, size, file_root):
    length = len(clusters_before)
    changes_histogram = {}
    for i in range(-size * size, size * size):
        changes_histogram[i] = 0

    for i in tqdm(range(length)):
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

    fp = open("outputs\\" + file_root + "cd.txt", "w")
    fp.write(output_string)
    fp.close()


def cluster_sde(clusters_before, clusters_after, file_root):
    cluster_changes = {}
    length = len(clusters_before)

    for i in tqdm(range(length)):
        affected_cluster = max(clusters_before[i])
        resulting_cluster = max(clusters_after[i])
        change = resulting_cluster - affected_cluster

        if affected_cluster in cluster_changes:
            cluster_changes[affected_cluster].append(change)
        else:
            cluster_changes[affected_cluster] = [change]

    cluster_sizes = []
    drifts = []
    diffusions = []
    num_samples = []
    residues = []

    for cluster_size in sorted(cluster_changes.keys()):
        changes = cluster_changes[cluster_size]
        drift = sum(changes) / len(changes)
        diffusion = sum([(change - drift) ** 2 for change in changes]) / len(changes) - drift ** 2

        cluster_sizes.append(cluster_size)
        drifts.append(drift)
        diffusions.append(diffusion)
        num_samples.append(len(changes))

        if len(changes) > 100 and (cluster_size in [10, 30, 50, 100] or cluster_size % 200 == 0):
            residue_list = [int(change - drift) for change in changes]
            min_bin = min(residue_list) - 1
            max_bin = max(residue_list) + 1

            freq, bins = histogram(residue_list, bins=[i for i in range(min_bin, max_bin + 1)])
            residues.append({
                "size": i,
                "min_bin": min_bin,
                "max_bin": max_bin,
                "freq": freq
            })

    output_string = ""
    for i, cluster_size in enumerate(cluster_sizes):
        output_string += f"{cluster_size} {drifts[i]} {diffusions[i]} {num_samples[i]}\n"
    
    fp = open("outputs\\" + file_root + "sde.txt", "w")
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
        file_name = f"temp\\{file_root}{i}_landscape.txt"
        landscape = loadtxt(file_name, dtype=bool)
        landscapes.append(landscape)

        file_name = f"temp\\{file_root}{i}_dynamics.txt"
        raw_data = open(file_name, "r").read()
        lines = raw_data.split("\n")

        for line in lines[:-1]:
            line_split = line.split(":")
            clusters_before.append(list(map(int, line_split[0].split())))
            clusters_after.append(list(map(int, line_split[1].split())))

    print("Calculating cluster size distribution ...")
    cluster_size_distribution(landscapes, file_root)

    print("Calculating cluster dynamics ...")
    cluster_dynamics(clusters_before, clusters_after, landscape.shape[0], file_root)

    print("Calculating cluster SDE ...")
    cluster_sde(clusters_before, clusters_after, file_root)


if __name__ == '__main__':
    simulation_name = "tdp"
    num_simulations = 4
    parameters = [0.7, 0]

    analysis(simulation_name, num_simulations, parameters)