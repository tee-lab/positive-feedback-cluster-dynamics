# NUMBER OF PROCESSES

from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from numpy import loadtxt, transpose
from tqdm import tqdm
from utils import get_file_root

from fig_constants import *


def load_processes(model_name, dataset, param, samples_cutoff):
    base_path = f"./results"
    file_root = get_file_root(model_name, param)
    file_name = f"{base_path}/{model_name}/{dataset}/{file_root}/{file_root}_sde.txt"
    data = transpose(loadtxt(file_name, dtype=float))
    num_samples = data[3][:]

    file_name = f"{base_path}/{model_name}/{dataset}/{file_root}/{file_root}_processes.txt"
    data = transpose(loadtxt(file_name, dtype=float))
    cluster_sizes, growth, decay, merge, split = data

    limit = -1
    for i in range(len(cluster_sizes)):
        if num_samples[i] < samples_cutoff:
            limit = i
            break
    if limit == -1:
        limit = 10

    return cluster_sizes[:limit], growth[:limit], decay[:limit], merge[:limit], split[:limit]


def fig7(main_fig):
    base_path = f"./results"
    null_dataset = "256x256_64"

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
        datasets.append("256x256_64")
        params.append([[0.65, 0], [0.7, 0], [0.72, 0]])
        variables.append("p")
        densities.append([0.27, 0.48, 0.54])

        model_names.append("tdp")
        display_names.append("Medium positive feedback")
        datasets.append("256x256_64")
        params.append([[0.51, 0.5], [0.535, 0.5], [0.55, 0.5]])
        variables.append("p")
        densities.append([0.25, 0.45, 0.53])

        model_names.append("scanlon")
        display_names.append("Extended positive feedback")
        datasets.append("256x256_64_8_24")
        params.append([[500], [770], [850]])
        variables.append("rainfall")
        densities.append([0.26, 0.49, 0.56])
    else:
        model_names.append("tdp")
        display_names.append("TDP (q = 0.25)")
        datasets.append("256x256_64")
        params.append([[0.585, 0.25], [0.62, 0.25], [0.645, 0.25]])
        variables.append("p")
        densities.append([0.24, 0.45, 0.52])

        model_names.append("tdp")
        display_names.append("TDP (q = 0.75)")
        datasets.append("256x256_64")
        params.append([[0.405, 0.75], [0.41, 0.75], [0.42, 0.75]])
        variables.append("p")
        densities.append([0.24, 0.38, 0.52])

        model_names.append("tdp")
        display_names.append("TDP (q = 0.92)")
        datasets.append("256x256_64")
        params.append([[0.282, 0.92], [0.283, 0.92], [0.2845, 0.92]])
        variables.append("p")

    num_rows = len(model_names)
    num_cols = 3
    fig, axs = plt.subplots(nrows=num_rows, ncols=1, constrained_layout=True, figsize=(8.27, 8.27 * num_rows / num_cols + 2))
    fig.suptitle('Number of Processes', fontsize=main_title_size)
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

        subfig.suptitle(display_name, x=0.08, ha="left", fontweight="bold", fontsize=row_title_size)
        axs = subfig.subplots(nrows=1, ncols=num_cols)

        for col, ax in enumerate(axs):
            ax.set_title(chr(65 + row) + str(col + 1), loc="left")

            cluster_sizes, growth, decay, merge, split = load_processes(model_name, dataset, param[col], samples_cutoff)
            # null_cluster_sizes, null_merge, null_split = load_drift("null_model", null_dataset, [density[col]], 100)

            ax.loglog(cluster_sizes, merge, "b-")
            ax.loglog(cluster_sizes, split, "r-")
            ax.loglog(cluster_sizes, growth, "b--")
            ax.loglog(cluster_sizes, decay, "r--")

            ax_inset = ax.inset_axes([0.2, 0.1, 0.4, 0.4])
            ax_inset.semilogy(cluster_sizes, merge, "b-")
            ax_inset.semilogy(cluster_sizes, split, "r-")
            ax_inset.semilogy(cluster_sizes, growth, "b--")
            ax_inset.semilogy(cluster_sizes, decay, "r--")

            if row == num_rows - 1:
                ax.set_xlabel("cluster size s")
            else:
                ax.set_xticklabels([])
                ax.set_xticks([])

            if col == 0:
                ax.set_xlim(1, 10 ** 3)
            elif col == 1:
                ax.set_xlim(1, 10 ** 4)
            else:
                ax.set_xlim(1, 10 ** 4.5)
                
            if col == 0:
                ax.set_ylabel("Frequency")

            if row == 0 and col == num_cols - 1:
                blue_line = Line2D([0], [0], color="blue", label="merge")
                red_line = Line2D([0], [0], color="red", label="split")
                blue_dotted_line = Line2D([0], [0], color="blue", linestyle='--', label="growth")
                red_dotted_line = Line2D([0], [0], color="red", linestyle='--', label="decay")
                ax.legend(handles=[blue_line, red_line, blue_dotted_line, red_dotted_line])

    if main_fig:
        fig_name = f"./figures/fig7_{null_dataset}.png"
    else:
        fig_name = f"./figures/fig7_{null_dataset}_appendix.png"

    plt.savefig(fig_name, bbox_inches="tight")