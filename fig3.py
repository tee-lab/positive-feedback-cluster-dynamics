from matplotlib import pyplot as plt
from numpy import loadtxt, transpose
from tqdm import tqdm
from utils import get_file_root


def load_drift(model_name, dataset, param, limit):
    file_root = get_file_root(model_name, param)
    file_name = f"{base_path}/{model_name}/{dataset}/{file_root}/{file_root}_sde.txt"
    data = transpose(loadtxt(file_name, dtype=float))
    cluster_sizes, drift, num_samples = data[0], data[1], data[3]

    if model_name != "null_model":
        return cluster_sizes[:limit], drift[:limit]
    else:
        limit = -1
        for i in range(len(cluster_sizes)):
            if num_samples[i] < samples_cutoff:
                limit = i
                break
        if limit == -1:
            limit = 10

        return cluster_sizes[:limit], drift[:limit]


if __name__ == '__main__':
    base_path = f"./results"
    null_dataset = "100x100_23"
    samples_cutoff = 5000

    model_names = []
    display_names = []
    datasets = []
    params = []
    variables = []
    densities = []
    phase_diagram_files = []

    model_names.append("tdp")
    display_names.append("Low positive feedback")
    datasets.append("100x100_23")
    params.append([[0.65, 0], [0.7, 0], [0.72, 0]])
    variables.append("p")
    densities.append([0.27, 0.48, 0.54])
    phase_diagram_files.append("q0_transitions.txt")

    model_names.append("tdp")
    display_names.append("Medium positive feedback")
    datasets.append("100x100_23")
    params.append([[0.51, 0.5], [0.535, 0.5], [0.55, 0.5]])
    variables.append("p")
    densities.append([0.25, 0.45, 0.53])
    phase_diagram_files.append("q0p5_transitions.txt")

    model_names.append("scanlon")
    display_names.append("Extended positive feedback")
    datasets.append("100x100_23_6_24")
    params.append([[500], [770], [850]])
    variables.append("rainfall")
    densities.append([0.26, 0.49, 0.56])
    phase_diagram_files.append("transitions.txt")

    num_rows = len(model_names)
    num_cols = 3
    fig, axs = plt.subplots(nrows=num_rows, ncols=1, constrained_layout=True, figsize=(8.27, 8.27 * num_rows / num_cols + 2))
    fig.suptitle('Growth Rate of Clusters')

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
        phase_diagram_file = phase_diagram_files[row]

        subfig.suptitle(display_name, x=0.08, ha="left")
        axs = subfig.subplots(nrows=1, ncols=num_cols)

        for col, ax in enumerate(axs):
            ax.set_title(chr(65 + row) + str(col + 1), loc="left")
            ax.axhline(y=0, linestyle="--", color="k")

            if col == 0:
                limit = 100
            elif col == 1:
                limit = 1000
            else:
                limit = 4000

            cluster_sizes, drift = load_drift(model_name, dataset, param[col], limit)
            null_cluster_sizes, null_drift = load_drift("null_model", null_dataset, [density[col]], limit)

            if row == 0 and col == 0:
                ax.plot(cluster_sizes, drift, "b-", label="Model")
                ax.plot(null_cluster_sizes, null_drift, "0.7", label="Null model")
            else:
                ax.plot(cluster_sizes, drift, "b-")
                ax.plot(null_cluster_sizes, null_drift, "0.7")

            if row == num_rows - 1:
                ax.set_xlabel("cluster size s")
            else:
                ax.set_xticklabels([])
                ax.set_xticks([])
                
            if col == 0:
                ax.set_ylabel("mean growth rate")

    fig.legend(["model", "null"], loc='upper right')
    plt.savefig(f"./figures/fig3_{null_dataset}.png")