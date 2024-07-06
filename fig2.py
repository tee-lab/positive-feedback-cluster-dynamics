from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from numpy import array, delete, loadtxt, transpose, zeros
from utils import get_file_root
from tqdm import tqdm


def load_cd(model_name, dataset, param):
    file_root = get_file_root(model_name, param)
    file_name = f"{base_path}/{model_name}/{dataset}/{file_root}/{file_root}_cd.txt"
    data = transpose(loadtxt(file_name, dtype=int))
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

    abs_changes = []
    abs_freqs = []

    for key in sorted(abs_changes_histogram.keys()):
        abs_changes.append(key)
        abs_freqs.append(abs_changes_histogram[key])

    abs_freqs = array(abs_freqs)
    changes_icdf = zeros(len(abs_changes), dtype=int)
    for i in range(len(abs_changes)):
        changes_icdf[i] = abs_freqs[i:].sum()
    changes_icdf = changes_icdf / changes_icdf[0]

    trim_index = -1
    last_value = changes_icdf[-1]
    for i in range(len(abs_changes) - 1, -1, -1):
        if changes_icdf[i] != last_value:
            trim_index = i
            break

    # remove 0 and 1, remove last repeating values
    abs_changes = abs_changes[2:trim_index + 1]
    changes_icdf = changes_icdf[2:trim_index + 1]

    return abs_changes, changes_icdf


if __name__ == '__main__':
    base_path = f"./results"
    null_dataset = "256x256_64"
    main_fig = False

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

    num_rows = len(model_names)
    num_cols = 3
    fig, axs = plt.subplots(nrows=num_rows, ncols=1, constrained_layout=True, figsize=(8.27, 8.27 * num_rows / num_cols + 2))
    fig.suptitle('Cluster Dynamics: Distribution of Changes in Cluster Sizes')

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

        subfig.suptitle(display_name, x=0.08, ha="left")
        axs = subfig.subplots(nrows=1, ncols=num_cols)

        for col, ax in enumerate(axs):
            ax.set_title(chr(65 + row) + str(col + 1), loc="left")

            cluster_sizes, changes_icdf = load_cd(model_name, dataset, param[col])
            null_cluster_sizes, null_changes_icdf = load_cd("null_model", null_dataset, [density[col]])

            if row == 0 and col == 0:
                ax.loglog(cluster_sizes, changes_icdf, "b-", label="Model")
                ax.loglog(null_cluster_sizes, null_changes_icdf, "0.7", label="Null model")
            else:
                ax.loglog(cluster_sizes, changes_icdf, "b-")
                ax.loglog(null_cluster_sizes, null_changes_icdf, "0.7")

            if col == 0:
                ax.set_ylabel("$P(\Delta S \geq \Delta s)$")
            if row == num_rows - 1:
                ax.set_xlabel("change in cluster size $\Delta s$")

            if null_dataset == "100x100_23":
                ax.set_ylim(1e-8, 1)

                if col == 0:
                    ax.set_xlim(1, 10 ** 2.5)
                elif col == 1:
                    ax.set_xlim(1, 10 ** 3.5)
                else:
                    ax.set_xlim(1, 10 ** 4)

            elif null_dataset == "256x256_64":
                ax.set_ylim(1e-10, 1)

                if col == 0:
                    ax.set_xlim(1, 10 ** 3)
                elif col == 1:
                    ax.set_xlim(1, 10 ** 4)
                else:
                    ax.set_xlim(1, 10 ** 5.5)

            if col != 0:
                ax.set_yticklabels([])
                ax.set_yticks([])
            
            if row != num_rows - 1:
                ax.set_xticklabels([])
                ax.set_xticks([])

            if row == 0 and col == num_cols - 1:
                blue_line = Line2D([0], [0], color="blue", label="model")
                grey_line = Line2D([0], [0], color="0.7", label="null")
                ax.legend(handles=[blue_line, grey_line])

    if main_fig:
        fig_name = f"./figures/fig2_{null_dataset}.png"
    else:
        fig_name = f"./figures/fig2_{null_dataset}_appendix.png"

    plt.savefig(fig_name)