from multiprocessing import set_start_method, Pool
from os import name, system
from subprocess import run


def process(simulation_name, simulation_index, parameters):
    if simulation_name == "tdp":
        p = parameters[0]
        q = parameters[1]

        if name == "nt":
            run(f"tdp.exe {p} {q} {simulation_index}", shell=True)
        else:
            run(f"./tdp {p} {q} {simulation_index}", shell=True)


if __name__ == '__main__':
    set_start_method('spawn')
    simulation_name = "tdp"
    parameters = [0.29, 0.92]
    num_simulations = 4

    if simulation_name == "tdp":
        system(f"gcc tdp.c -o tdp")  

    with Pool(num_simulations) as p:
        p.starmap(process, [(simulation_name, i, parameters) for i in range(num_simulations)])