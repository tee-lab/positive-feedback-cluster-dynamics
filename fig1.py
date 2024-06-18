from matplotlib import pyplot as plt
from numpy import delete, loadtxt, transpose, zeros
from utils import get_file_root
from tqdm import tqdm


def load_csd(model_name, dataset, param):
    file_root = get_file_root(model_name, param)
    file_name = f"{base_path}/{model_name}/{dataset}/{file_root}/{file_root}_csd.txt"
    data = transpose(loadtxt(file_name, dtype=int))
    cluster_sizes, frequencies = data[0], data[1]
    cluster_icdf = zeros(len(cluster_sizes), dtype=int)

    for i in range(len(cluster_sizes)):
        cluster_icdf[i] = frequencies[i:].sum()
    cluster_icdf = cluster_icdf / cluster_icdf[0]

    remove_indices = []
    for i in range(len(cluster_sizes) - 1):
        if cluster_icdf[i] == cluster_icdf[i + 1]:
            remove_indices.append(i)

    cluster_sizes = delete(cluster_sizes, remove_indices)
    cluster_icdf = delete(cluster_icdf, remove_indices)

    return cluster_sizes, cluster_icdf


if __name__ == '__main__':
    base_path = f"./results"
    null_dataset = "100x100_23"

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
    num_cols = 4
    fig, axs = plt.subplots(nrows=num_rows, ncols=1, constrained_layout=True, figsize=(8.27, 8.27 * num_rows / num_cols + 2))
    fig.suptitle('Cluster Size Distribution')

    # clear subplots
    for ax in axs:
        ax.remove()

    # add subfigure per subplot
    gridspec = axs[0].get_subplotspec().get_gridspec()
    subfigs = [fig.add_subfigure(gs) for gs in gridspec]

    for row, subfig in tqdm(enumerate(subfigs)):
        model_name = model_names[row]
        display_name = display_names[row]
        dataset = datasets[row]
        param = params[row]
        variable = variables[row]
        density = densities[row]
        phase_diagram_file = phase_diagram_files[row]

        subfig.suptitle(display_name, x=0.065, ha="left")
        axs = subfig.subplots(nrows=1, ncols=num_cols)
        for col, ax in enumerate(axs):
            if col == 0:
                phase_diagram = transpose(loadtxt(f"{base_path}/{model_name}/{phase_diagram_file}"))
                ax.plot(phase_diagram[0], phase_diagram[1], "k-")
                ax.set_title(chr(65 + row), loc="left")
                ax.set_xlabel(variable)
                ax.set_ylabel("density")

                ax.plot([par[0] for par in param], density, "rx")
                annotations = [chr(65 + row) + str(i) for i in range(1, num_cols)]
                for j in range(len(annotations)):
                    ax.annotate(annotations[j], (param[j][0], density[j]))
            else:
                ax.set_title(chr(65 + row) + str(col), loc="left")  

                cluster_sizes, cluster_icdf = load_csd(model_name, dataset, param[col - 1])
                ax.loglog(cluster_sizes, cluster_icdf, "b-", label="model")

                null_cluste_sizes, null_cluster_icdf = load_csd("null_model", null_dataset, [density[col - 1]])
                ax.loglog(null_cluste_sizes, null_cluster_icdf, "0.7", label="null")

                ax.set_ylim(10 ** -4, 1)
                if col == 1:
                    ax.set_ylabel("$P(S \geq s)$")
                else:
                    ax.set_ylabel("")
                    ax.set_yticklabels([])
                    ax.set_yticks([])

                if row == num_rows - 1:
                    ax.set_xlabel("cluster size s")
            
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right')
    plt.savefig(f"./figures/fig1_{null_dataset}.png")