from matplotlib import pyplot as plt
from numpy import zeros
from numpy.random import randint
from skimage.measure import label


def delete_files_in_dir(path):
    import os
    for file in os.listdir(path):
        os.remove(path + file)


def left_trim(list):
    trim_index = -1
    for i in range(len(list)):
        if list[i] != 0:
            trim_index = i
            break

    return list[trim_index:]


def right_trim(list):
    trim_index = -1
    for i in range(len(list) - 1, -1, -1):
        if list[i] != 0:
            trim_index = i
            break

    return list[:trim_index + 1]
    

def get_csd(landscape):
    labelled_landscape = apply_periodic_boundary(label(landscape, background=0, connectivity=1))
    size = landscape.shape[0]
    num_clusters = labelled_landscape.max()
    clusters_histogram = zeros((size * size + 1), dtype=int)

    clusters_histogram[0] = (size * size) - (labelled_landscape > 0).sum()
    for cluster_index in range(1, num_clusters + 1):
        cluster_size = (labelled_landscape == cluster_index).sum()
        clusters_histogram[cluster_size] += 1

    return clusters_histogram


def apply_periodic_boundary(labels):
    length = len(labels)

    for i in range(length):
        if labels[i, 0] != 0 and labels[i, -1] != 0 and labels[i, 0] != labels[i, -1]:
            new_label = labels[i, 0]
            old_label = labels[i, -1]
            labels[labels == old_label] = new_label
    
    for j in range(length):
        if labels[0, j] != 0 and labels[-1, j] != 0 and labels[0, j] != labels[-1, j]:
            new_label = labels[0, j]
            old_label = labels[-1, j]
            labels[labels == old_label] = new_label

    return labels


def get_file_root(simulation_name, parameters):
    if simulation_name == "tdp":
        p = parameters[0]
        q = parameters[1]
        file_root = f"tdp_{str(p).replace('.', 'p')}_{str(q).replace('.', 'q')}"
    elif simulation_name == "scanlon":
        rainfall = parameters[0]
        file_root = f"scanlon_{str(rainfall).replace('.', 'p')}"
    elif simulation_name == "null_model":
        f = parameters[0]
        file_root = f"null_{str(f).replace('.', 'p')}"

    return file_root


if __name__ == '__main__':
    delete_files_in_dir("temp/")