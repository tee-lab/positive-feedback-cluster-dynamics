from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from numpy import array
from tqdm import tqdm
from utils import get_file_root


def load_residues(model_name, dataset, param, cluster_size_req):
    file_root = get_file_root(model_name, param)
    file_name = f"{base_path}/{model_name}/{dataset}/{file_root}/{file_root}_residues.txt"
    fp = open(file_name, "r")
    lines = fp.read().split("\n")

    for line in lines[:-1]:
        section1, section2, section3 = line.split(" : ")
        cluster_size = int(section1)

        if cluster_size == cluster_size_req:
            bins = list(map(int, section2.split(", ")))
            freqs = array(list(map(int, section3.split(", "))))
            bin_range = list(range(bins[0], bins[1]))

            zero_index = -1
            for i in range(len(bin_range)):
                if bin_range[i] == 0:
                    zero_index = i
                    break

            bin_range = bin_range[zero_index:]
            freqs = freqs[zero_index:] / sum(freqs[zero_index:])

            return bin_range, freqs
        
    return None


if __name__ == '__main__':
    base_path = f"./results"
    null_dataset = "256x256_64"
    cluster_size = 100
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
    fig.suptitle(f'Distribution of residues for cluster size {cluster_size}')

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

            residues, freqs = load_residues(model_name, dataset, param[col], cluster_size)
            null_result = load_residues("null_model", null_dataset, [density[col]], cluster_size)

            if row == 0 and col == 0:
                ax.loglog(residues, freqs, "bo", label="Model")
                if null_result is not None:
                    null_residues, null_freqs = null_result
                    ax.loglog(null_residues, null_freqs, "ko", label="Null model")
            else:
                ax.loglog(residues, freqs, "bo")
                if null_result is not None:
                    null_residues, null_freqs = null_result
                    ax.loglog(null_residues, null_freqs, "ko")

            if row == num_rows - 1:
                ax.set_xlabel("residues")
            if col == 0:
                ax.set_ylabel("fraction")

            ax.set_ylim(10 ** -7, 1)
            if col != 0:
                ax.set_yticklabels([])
                ax.set_yticks([])

            if cluster_size == 10:
                ax.set_xlim(1, 10 ** 1.5)
            elif cluster_size == 50:
                ax.set_xlim(1, 10 ** 2)
            elif cluster_size == 100:
                ax.set_xlim(1, 10 ** 2.5)

            if row != num_rows - 1:
                ax.set_xticklabels([])
                ax.set_xticks([])

            if row == 0 and col == num_cols - 1:
                blue_dot = Line2D([0], [0], color="blue", marker="o", linestyle="", label="model")
                black_dot = Line2D([0], [0], color="black", marker="o", linestyle="", label="null")
                ax.legend(handles=[blue_dot, black_dot])

    if main_fig:
        fig_name = f"./figures/fig5_{null_dataset}_{cluster_size}.png"
    else:
        fig_name = f"./figures/fig5_{null_dataset}_{cluster_size}_appendix.png"

    plt.savefig(fig_name)