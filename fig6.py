# ABRUPT PROCESSES

from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from numpy import loadtxt, transpose
from tqdm import tqdm
from utils import get_file_root

from fig_constants import *


def load_abrupt(model_name, dataset, param, samples_cutoff):
    base_path = f"./results"
    file_root = get_file_root(model_name, param)
    file_name = f"{base_path}/{model_name}/{dataset}/{file_root}/{file_root}_sde.txt"
    data = transpose(loadtxt(file_name, dtype=float))
    num_samples = data[3][:]

    file_name = f"{base_path}/{model_name}/{dataset}/{file_root}/{file_root}_abrupt.txt"
    data = transpose(loadtxt(file_name, dtype=float))
    cluster_sizes, merge, split = data[0], data[1], data[2]

    limit = -1
    for i in range(len(cluster_sizes)):
        if num_samples[i] < samples_cutoff:
            limit = i
            break
    if limit == -1:
        limit = 10

    return cluster_sizes[:limit], merge[:limit], split[:limit]


def fig6(model_dataset, scanlon, null_dataset, main_fig):
    base_path = f"./results"

    if null_dataset == "100x100_23":
        samples_cutoff = 5000
    elif null_dataset == "256x256_64":
        samples_cutoff = 1000

    model_names = []
    display_names = []
    datasets = []
    params = []
    variables = []
    densities = []

    if main_fig:
        model_names.append("tdp")
        display_names.append("Low positive feedback")
        datasets.append(model_dataset)
        params.append([[0.65, 0], [0.7, 0], [0.72, 0]])
        variables.append("p")
        densities.append([0.27, 0.48, 0.54])

        model_names.append("tdp")
        display_names.append("Medium positive feedback")
        datasets.append(model_dataset)
        params.append([[0.51, 0.5], [0.535, 0.5], [0.55, 0.5]])
        variables.append("p")
        densities.append([0.25, 0.45, 0.53])

        model_names.append("scanlon")
        display_names.append("Extended positive feedback")
        datasets.append(model_dataset + "_" + scanlon)
        params.append([[500], [770], [850]])
        variables.append("rainfall")
        densities.append([0.26, 0.49, 0.56])
    else:
        model_names.append("tdp")
        display_names.append("TDP (q = 0.25)")
        datasets.append(model_dataset)
        params.append([[0.585, 0.25], [0.62, 0.25], [0.645, 0.25]])
        variables.append("p")
        densities.append([0.24, 0.45, 0.52])

        model_names.append("tdp")
        display_names.append("TDP (q = 0.75)")
        datasets.append(model_dataset)
        params.append([[0.405, 0.75], [0.41, 0.75], [0.42, 0.75]])
        variables.append("p")
        densities.append([0.24, 0.38, 0.52])

    num_rows = len(model_names)
    num_cols = 3
    fig, axs = plt.subplots(nrows=num_rows, ncols=1, constrained_layout=True, figsize=(8.27, 8.27 * num_rows / num_cols + 2))
    fig.suptitle('Average Change associated with Merges and Splits', fontsize=main_title_size)
    plt.rc("axes", labelsize=label_size)

    # clear subplots
    for ax in axs:
        ax.remove()

    gridspec = axs[0].get_subplotspec().get_gridspec()
    subfigs = [fig.add_subfigure(gs) for gs in gridspec]

    for row, subfig in enumerate(tqdm(subfigs)):
        model_name = model_names[row]
        display_name = display_names[row]
        dataset = datasets[row]
        param = params[row]
        variable = variables[row]
        density = densities[row]

        subfig.suptitle(display_name, x=0.08, ha="left", fontweight="bold", fontsize=row_title_size)
        axs = subfig.subplots(nrows=1, ncols=num_cols)

        for col, ax in enumerate(axs):
            ax.set_title(chr(65 + row) + str(col + 1), loc="left")
            cluster_sizes, merge, split = load_abrupt(model_name, dataset, param[col], samples_cutoff)
            ax.plot(cluster_sizes, merge, "b-")
            ax.plot(cluster_sizes, -split, "r-")

            if row == num_rows - 1:
                ax.set_xlabel("cluster size s")
                
            if col == 0:
                ax.set_ylabel("Average change")

            if row == 0 and col == num_cols - 1:
                blue_line = Line2D([0], [0], color="blue", label="merge")
                red_line = Line2D([0], [0], color="red", label="split")
                ax.legend(handles=[blue_line, red_line])

    if main_fig:
        fig_name = f"./figures/fig6_{null_dataset}.png"
    else:
        fig_name = f"./figures/fig6_{null_dataset}_appendix.png"

    plt.savefig(fig_name, bbox_inches="tight")