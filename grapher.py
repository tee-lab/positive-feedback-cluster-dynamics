from matplotlib import pyplot as plt
from numpy import delete, loadtxt, transpose, zeros


def plot_csd(data_path, file_root):
    file_name = data_path + file_root + "csd.txt"
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

    plt.title("Cluster Size Distribution")
    plt.xlabel("Cluster Size s")
    plt.ylabel(r"P(S \\gt s)")
    plt.loglog(cluster_sizes, cluster_icdf, "o")
    plt.savefig(data_path + file_root + "csd.png")
    plt.show()


def grapher(simulation_name, parameters, data_path = "outputs/"):
    if simulation_name == "tdp":
        p = parameters[0]
        q = parameters[1]
        file_root = f"tdp_{str(p).replace('.', 'p')}_{str(q).replace('.', 'q')}_"

    plot_csd(data_path, file_root)


if __name__ == '__main__':
    simulation_name = "tdp"
    parameters = [0.7, 0]
    grapher(simulation_name, parameters)