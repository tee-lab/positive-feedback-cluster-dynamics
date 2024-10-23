from multiprocessing import Pool
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

    fp = open("outputs/" + file_root + "csd.txt", "w")
    fp.write(output_string)
    fp.close()

    densities = []
    for landscape in landscapes:
        densities.append(landscape.sum() / (size * size))

    output_string = ""
    for i in range(len(densities)):
        output_string += f"{i} {densities[i]}\n"
    
    fp = open("outputs/" + file_root + "densities.txt", "w")
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

    fp = open("outputs/" + file_root + "cd.txt", "w")
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
    drifts, diffusions = [], []
    num_samples, residues = [], []
    growth_probabilities, decay_probabilities = [], []
    num_growths, num_decays, num_merges, num_splits = [], [], [], []
    avg_merge_change, avg_split_change = [], []

    for cluster_size in tqdm(sorted(cluster_changes.keys())):
        changes = array(cluster_changes[cluster_size])
        drift = changes.mean()
        diffusion = ((changes - drift) ** 2).mean()

        cluster_sizes.append(cluster_size)
        drifts.append(drift)
        diffusions.append(diffusion)
        num_samples.append(len(changes))
        growth_probabilities.append(sum(changes > 0) / len(changes))
        decay_probabilities.append(sum(changes < 0) / len(changes))
        num_growths.append(sum(changes == 1))
        num_decays.append(sum(changes == -1))
        num_merges.append(sum(changes > 1))
        num_splits.append(sum(changes < 1))

        if num_merges[-1] != 0:
            avg_merge_change.append(sum([change for change in changes if change > 1]) / num_merges[-1])
        else:
            avg_merge_change.append(0)
        if num_splits[-1] != 0:
            avg_split_change.append(sum([change for change in changes if change < -1]) / num_splits[-1])
        else:
            avg_split_change.append(0)

        # if len(changes) > 100:
        if len(changes) > 100 and cluster_size in [10, 30, 50, 100, 200, 500]:
            residue_list = [int(change - drift) for change in changes]
            min_bin = min(residue_list) - 1
            max_bin = max(residue_list) + 1

            freq, bins = histogram(residue_list, bins=[i for i in range(min_bin, max_bin + 1)])
            residues.append({
                "size": cluster_size,
                "min_bin": min_bin,
                "max_bin": max_bin,
                "freq": freq
            })

    output_string = ""
    for i, cluster_size in enumerate(cluster_sizes):
        output_string += f"{cluster_size} {drifts[i]} {diffusions[i]} {num_samples[i]}\n"
    
    fp = open("outputs/" + file_root + "sde.txt", "w")
    fp.write(output_string)
    fp.close()

    output_string = ""
    for i, cluster_size in enumerate(cluster_sizes):
        output_string += f"{cluster_size} {round(growth_probabilities[i], 4)} {round(decay_probabilities[i], 4)}\n"

    fp = open("outputs/" + file_root + "gd.txt", "w")
    fp.write(output_string)
    fp.close()

    output_string = ""
    for i, cluster_size in enumerate(cluster_sizes):
        output_string += f"{cluster_size} {num_growths[i]} {num_decays[i]} {num_merges[i]} {num_splits[i]}\n"

    fp = open("outputs/" + file_root + "processes.txt", "w")
    fp.write(output_string)
    fp.close()

    output_string = ""
    for i, cluster_size in enumerate(cluster_sizes):
        output_string += f"{cluster_size} {avg_merge_change[i]} {avg_split_change[i]}\n"

    fp = open("outputs/" + file_root + "abrupt.txt", "w")
    fp.write(output_string)
    fp.close()

    fp = open("outputs/" + file_root + "residues.txt", "w")
    output_string = ""
    for info in residues:
        output_string += f"{info['size']} : {info['min_bin']}, {info['max_bin']} : {', '.join([str(val) for val in info['freq']])}\n"
    fp.write(output_string)
    fp.close()


def read_file(file_root, simulation_index):
    file_name = f"temp/{file_root}{simulation_index}_landscape.txt"
    landscape = loadtxt(file_name, dtype=bool)

    clusters_before = []
    clusters_after = []

    file_name = f"temp/{file_root}{simulation_index}_dynamics.txt"
    raw_data = open(file_name, "r").read()
    lines = raw_data.split("\n")

    if simulation_index == 0:
        iterator = tqdm(range(len(lines) - 1))
    else:
        iterator = range(len(lines) - 1)

    for line_index in iterator:
        line_split = lines[line_index].split(":")
        clusters_before.append(list(map(int, line_split[0].split())))
        clusters_after.append(list(map(int, line_split[1].split())))

    return landscape, clusters_before, clusters_after


def analysis(simulation_name, num_simulations, parameters):
    clusters_before = []
    clusters_after = []
    landscapes = []

    if simulation_name == "tdp":
        p = parameters[0]
        q = parameters[1]
        file_root = f"tdp_{str(p).replace('.', 'p')}_{str(q).replace('.', 'q')}_"
    elif simulation_name == "scanlon":
        rainfall = parameters[0]
        file_root = f"scanlon_{str(rainfall).replace('.', 'p')}_"
    elif simulation_name == "null":
        f = parameters[0]
        file_root = f"null_{str(f).replace('.', 'p')}_"

    print("Reading files ...")
    with Pool(num_simulations) as p:
        data = p.starmap(read_file, [(file_root, i) for i in range(num_simulations)])

    for landscape, clusters_before_i, clusters_after_i in data:
        landscapes.append(landscape)
        clusters_before += clusters_before_i
        clusters_after += clusters_after_i

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