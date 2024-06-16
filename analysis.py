from numpy import loadtxt, zeros
from os import path
from pickle import dump
from skimage.measure import label

from utils import *


def cluster_size_distribution(landscapes, file_root):
    size = landscapes[0].shape[0]
    clusters_histogram = zeros(size * size, dtype=int)
    for landscape in landscapes:
        clusters_histogram += get_csd(landscape)[1:]
    clusters_histogram = trim_list(clusters_histogram)
    
    output_string = ""
    for i in range(len(clusters_histogram)):
        output_string += f"{i + 1} {clusters_histogram[i]}\n"

    fp = open("outputs/" + file_root + "csd.txt", "w")
    fp.write(output_string)
    fp.close()

    fp = open("outputs/" + file_root + "lattices.pkl", "wb")
    dump(landscapes, fp)
    fp.close()


def cluster_dynamics(clusters_before, clusters_after, file_root):
    pass


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


if __name__ == '__main__':
    simulation_name = "tdp"
    num_simulations = 4
    parameters = [0.7, 0]

    analysis(simulation_name, num_simulations, parameters)