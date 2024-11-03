"""
Version 2 of self consistency check
Wherein clusters are initially sampled from a randomly generated model
And a random cluster is selected from the pool of clusters to undergo a stochastic update, proportional to its size
"""


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


def init_csd_from_random_null(size = 256, ensembles = 1):
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
    biggest_cluster = int(max(clusters))
    cluster_sizes = range(1, biggest_cluster + 1)

    frequencies = [0 for _ in range(biggest_cluster)]
    for cluster in clusters:
        frequencies[int(cluster) - 1] += 1

    cluster_icdf = zeros(len(cluster_sizes), dtype=int)

    for i in range(len(cluster_sizes)):
        cluster_icdf[i] = sum(frequencies[i:])
    cluster_icdf = cluster_icdf / cluster_icdf[0]

    return cluster_sizes, cluster_icdf


def select_cluster(clusters_pool, total_area):
    r = random() * total_area
    cumsum = 0
    
    for i in range(len(clusters_pool)):
        cumsum += clusters_pool[i]
        if cumsum > r:
            return i
            
    return len(clusters_pool) - 1


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

    # load observed data
    file_name = data_path + file_root + "csd.txt"
    data = transpose(loadtxt(file_name, dtype=int))
    cluster_sizes, frequencies = data[0], data[1]
    observed_clusters = []
    for cluster, frequency in zip(cluster_sizes, frequencies):
        observed_clusters.extend([cluster for _ in range(frequency)])

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
    clusters_pool = init_csd_from_random_null(size=256, ensembles=1)
    samples = clusters_pool.copy()
    num_underflow, num_overflow = 0, 0
    num_steps = 100_000

    f = lambda x: a_fit * sqrt(x) + b_fit * x
    g = lambda x: sqrt(m_fit * x)
    print(f"Simulating with {len(clusters_pool)} clusters")

    # simulate SDEs for all clusters
    for _ in tqdm(range(num_steps)):
        total_area = sum(clusters_pool)
        cluster_index = select_cluster(clusters_pool, total_area)
        cluster = clusters_pool.pop(cluster_index)

        if int(cluster) in residues:
            noise = random_from_residue(residues[int(cluster)])
        else:
            num_overflow += 1
            continue

        change = f(cluster) + g(cluster) * noise

        if abs(change) < 1:
            # just a growth or a decay
            if change < 0:
                if cluster - change > 0:
                    clusters_pool.append(cluster - change)
                else:
                    num_underflow += 1
                    continue
            else:
                clusters_pool.append(cluster + change)
        elif change < -1:
            # a split
            if cluster - change > 0:
                cluster1 = cluster - change
                cluster2 = abs(change) - 1
                clusters_pool.append(cluster1)
                clusters_pool.append(cluster2)
            else:
                num_underflow += 1
                continue
        else:
            # a merge
            # merging_cluster = int(change)
            # diffs = [abs(merging_cluster - cluster) for cluster in clusters_pool]
            # min_diff = min(diffs)
            # min_index = diffs.index(min_diff)

            # clusters_pool.pop(min_index)
            clusters_pool.append(cluster + change)

    print(f"num_underflow: {num_underflow}, num_overflow: {num_overflow}, num_updates: {num_steps}")

    # plot simulation data
    sim_sizes, sim_icdf = get_icdf(clusters_pool)
    init_sizes, init_icdf = get_icdf(samples)
    obs_sizes, obs_icdf = get_icdf(observed_clusters)

    plt.figure()
    plt.title("Self consistency")
    plt.loglog(init_sizes, init_icdf, 'y.', label="simulation initial")
    plt.loglog(sim_sizes, sim_icdf, 'b.', label="simulation end")
    plt.loglog(obs_sizes, obs_icdf, 'r-', label="observed")
    plt.legend()
    plt.savefig(data_path + file_root + "sc3.png")
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

    for parameters in parameter_sets:
        base_path = f"results/{simulation_name}/{dataset}/"

        if simulation_name == "tdp":
            p = str(parameters[0]).replace('.', 'p')
            q = str(parameters[1]).replace('.', 'q')
            simulation_folder = f"tdp_{p}_{q}"
            base_path += f"{simulation_folder}/"

        self_consistency(simulation_name, parameters, base_path)