from matplotlib import pyplot as plt
from numpy import array, delete, loadtxt, transpose, zeros


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
    plt.ylabel("$P(S \geq s)$")
    plt.loglog(cluster_sizes, cluster_icdf, "o")
    plt.savefig(data_path + file_root + "csd.png")
    plt.show()
    plt.close()


def plot_cd(data_path, file_root):
    file_name = data_path + file_root + "cd.txt"
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

    plt.title("Cluster Dynamics (log-log)")
    plt.xlabel("$\Delta$s")
    plt.ylabel("$P(\Delta S \geq \Delta s)$")
    plt.loglog(abs_changes, changes_icdf)
    plt.savefig(data_path + file_root + "cd_loglog.png")
    plt.show()
    plt.close()

    plt.title("Cluster Dynamics (semilog-y)")
    plt.xlabel("$\Delta s$")
    plt.ylabel("$P(\Delta S \geq \Delta s)$")
    plt.semilogy(abs_changes, changes_icdf)
    plt.savefig(data_path + file_root + "cd_semilogy.png")
    plt.show()
    plt.close()


def plot_sde(data_path, file_root):
    file_name = data_path + file_root + "sde.txt"
    data = transpose(loadtxt(file_name, dtype=float))
    cluster_sizes, drifts, diffusions, num_samples = data[0], data[1], data[2], data[3]

    samples_cutoff = 5000
    index_cutoff = -1

    for i in range(len(num_samples)):
        if num_samples[i] < samples_cutoff:
            index_cutoff = i
            break

    if index_cutoff < 2:
        index_cutoff = 5

    cluster_sizes = cluster_sizes[:index_cutoff]
    drifts = drifts[:index_cutoff]
    diffusions = diffusions[:index_cutoff]
    
    plt.title("Drift")
    plt.xlabel("Cluster Size s")
    plt.ylabel("f(s)")
    plt.plot(cluster_sizes, drifts)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.savefig(data_path + file_root + "drift.png")
    plt.show()

    plt.title("Diffusion")
    plt.xlabel("Cluster Size s")
    plt.ylabel("$g^2 (s)$")
    plt.plot(cluster_sizes, diffusions)
    plt.savefig(data_path + file_root + "diffusion.png")
    plt.show()

    file_name = data_path + file_root + "gd.txt"
    data = transpose(loadtxt(file_name, dtype=float))
    cluster_sizes, growth_prob, decay_prob = data[0], data[1], data[2]

    plt.title("Growth and Decay Probabiities")
    plt.xlabel("Cluster Size s")
    plt.ylabel("Probability")
    plt.plot(cluster_sizes[:index_cutoff], growth_prob[:index_cutoff], label="Growth")
    plt.plot(cluster_sizes[:index_cutoff], decay_prob[:index_cutoff], label="Decay")
    plt.legend()
    plt.savefig(data_path + file_root + "gd.png")
    plt.show()
    plt.close()


def grapher(simulation_name, parameters, data_path = "outputs/"):
    if simulation_name == "tdp":
        p = parameters[0]
        q = parameters[1]
        file_root = f"tdp_{str(p).replace('.', 'p')}_{str(q).replace('.', 'q')}_"

    plot_csd(data_path, file_root)
    plot_cd(data_path, file_root)
    plot_sde(data_path, file_root)


if __name__ == '__main__':
    simulation_name = "tdp"
    parameters = [0.7, 0]
    grapher(simulation_name, parameters)