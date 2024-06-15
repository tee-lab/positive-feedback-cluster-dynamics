from multiprocessing import set_start_method, Pool
from os import system
from subprocess import run


def process(simulation_name, simulation_index, parameters):
    if simulation_name == "tdp":
        p = parameters[0]
        q = parameters[1]
        run(f"tdp_density.exe {p} {q} {simulation_index}", shell=True)


if __name__ == '__main__':
    set_start_method('spawn')
    simulation_name = "tdp"
    parameters = [0.7, 0]
    num_simulations = 8

    if simulation_name == "tdp":
        system(f"gcc tdp_density.c -o tdp_density")  

    with Pool(num_simulations) as p:
        p.starmap(process, [(simulation_name, i, parameters) for i in range(num_simulations)])