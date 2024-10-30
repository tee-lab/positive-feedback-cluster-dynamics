from matplotlib import pyplot as plt
from numpy import loadtxt, sqrt, sum, transpose, zeros
from random import choice, random
from scipy.optimize import curve_fit
from skimage.measure import label
from tqdm import tqdm


def fit_linear_through_origin(x, y):
    m = sum(x * y) / sum(x * x)
    return m


def specific_fit(x, a, b):
    return a * sqrt(x) + b * x


def random_from_residue(residue):
    dist = residue["dist"]
    r = random()
    cumsum = 0
    for i in range(len(dist)):
        cumsum  += dist[i]
        if r < cumsum:
            return i + residue["min_bin"] + 1
        
    return len(dist) + residue["min_bin"]


def init_csd_from_random_null(size = 256, ensembles = 64):
    cluster_sizes = []

    for _ in range(ensembles):
        lattice = zeros((size, size))

        for i in range(size):
            for j in range(size):
                if random() < 0.5:
                    lattice[i, j] = 1

        labelled_lattice = label(lattice, background=0, connectivity=1)
        
        for i in range(1, labelled_lattice.max() + 1):
            cluster_sizes.append(sum(sum(labelled_lattice == i)))

    return cluster_sizes


def get_icdf(clusters):
    biggest_cluster = max(clusters)
    cluster_sizes = range(1, biggest_cluster + 1)

    frequencies = [0 for _ in range(biggest_cluster)]
    for cluster in clusters:
        frequencies[cluster - 1] += 1

    cluster_icdf = zeros(len(cluster_sizes), dtype=int)

    for i in range(len(cluster_sizes)):
        cluster_icdf[i] = sum(frequencies[i:])
    cluster_icdf = cluster_icdf / cluster_icdf[0]

    return cluster_sizes, cluster_icdf


def self_consistency(simulation_name, parameters, data_path):
    if simulation_name == "tdp":
        p = parameters[0]
        q = parameters[1]
        file_root = f"tdp_{str(p).replace('.', 'p')}_{str(q).replace('.', 'q')}_"

    # read drift and diffusion
    file_path = data_path + file_root + "sde.txt"
    data = transpose(loadtxt(file_path, dtype=float))
    cluster_sizes, drift, diffusion, num_samples = data
    
    for i in range(len(cluster_sizes)):
        if num_samples[i] < samples_cutoff:
            cluster_sizes = cluster_sizes[:i]
            drift = drift[:i]
            diffusion = diffusion[:i]
            num_samples = num_samples[:i]
            break

    # fitting drift
    popt, _ = curve_fit(specific_fit, cluster_sizes, drift)
    a_fit, b_fit = popt
    fit_curve = specific_fit(cluster_sizes, a_fit, b_fit)

    # fitting diffusion
    m_fit = fit_linear_through_origin(cluster_sizes, diffusion)
    fit_line = m_fit * cluster_sizes

    plt.subplots(2, 2, figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.axhline(0, color='k', linestyle='--')
    plt.plot(cluster_sizes, drift, 'b.', label="drift data")
    plt.plot(cluster_sizes, fit_curve, 'r-', label=f"fit: y = {a_fit:.3f} sqrt(x) + {b_fit:.3f} x")
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(cluster_sizes, diffusion, 'b.', label="diffusion data")
    plt.plot(cluster_sizes, fit_line, 'r-', label=f"fit: y = {m_fit:.3f}x")
    plt.legend()
    plt.savefig(data_path + file_root + "sde_fit.png")
    plt.show()

    # read residues
    data = open(data_path + file_root + "residues.txt", "r").read().split("\n")
    residues = {}
    max_info = -1

    for line in data[:-1]:
        div1, div2, div3 = line.split(":")
        info = {}
        info["cluster_size"] = int(div1)
        min_bin, max_bin = map(int, div2.split(","))
        info["min_bin"] = min_bin
        info["max_bin"] = max_bin
        info["dist"] = list(map(int, div3.split(",")))
        info["dist"] = info["dist"] / sum(info["dist"])

        if int(div1) > max_info:
            max_info = int(div1)
        
        residues[info["cluster_size"]] = info

    # initialize SDE simulation
    clusters_pool = init_csd_from_random_null()
    samples = clusters_pool.copy()

    simul_time = 100
    dt = 0.01
    sqrt_dt = sqrt(dt)
    num_steps = int(simul_time / dt)

    f = lambda x: a_fit * sqrt(x) + b_fit * x
    g = lambda x: sqrt(m_fit * x)

    # simulate SDEs for all clusters
    for _ in tqdm(range(num_steps)):
        new_pool = []

        for cluster in clusters_pool:
            if cluster in residues:
                noise = random_from_residue(residues[cluster])
            else:
                noise = random_from_residue(residues[max_info])
                
            updated_cluster = f(cluster) * dt + g(cluster) * sqrt_dt + noise

            if updated_cluster < 1:
                updated_cluster = choice(samples)
            else:
                updated_cluster = int(updated_cluster)

            new_pool.append(updated_cluster)

        clusters_pool = new_pool

    # plot simulation data
    sim_sizes, sim_icdf = get_icdf(clusters_pool)
    plt.loglog(sim_sizes, sim_icdf, 'b.', label="simulation")

    # load observed data
    file_name = data_path + file_root + "csd.txt"
    data = transpose(loadtxt(file_name, dtype=int))
    cluster_sizes, frequencies = data[0], data[1]
    cluster_icdf = zeros(len(cluster_sizes), dtype=int)

    for i in range(len(cluster_sizes)):
        cluster_icdf[i] = frequencies[i:].sum()
    cluster_icdf = cluster_icdf / cluster_icdf[0]

    # plot observed data
    plt.title("Self consistency")
    plt.loglog(cluster_sizes, cluster_icdf, 'r.', label="observed")
    plt.legend()
    plt.savefig(data_path + file_root + "sc.png")
    plt.show()
    

if __name__ == '__main__':
    simulation_name = "tdp"
    dataset = "256x256_64"
    parameter_sets = [
        [0.7, 0],
        [0.65, 0],
        [0.51, 0.5],
        [0.535, 0.5]
    ]
    samples_cutoff = 100000

    base_path = f"results/{simulation_name}/{dataset}/"

    for parameters in parameter_sets:
        if simulation_name == "tdp":
            p = str(parameters[0]).replace('.', 'p')
            q = str(parameters[1]).replace('.', 'q')
            simulation_folder = f"tdp_{p}_{q}"
            base_path += f"{simulation_folder}/"

        self_consistency(simulation_name, parameters, base_path)