from multiprocessing import set_start_method, Pool
from os import makedirs, name, system
from subprocess import run

from analysis import analysis
from grapher import grapher


def process(simulation_name, simulation_index, parameters):
    if simulation_name == "tdp":
        p = parameters[0]
        q = parameters[1]
        file_root = f"temp\\tdp_{str(p).replace('.', 'p')}_{str(q).replace('.', 'q')}_{simulation_index}_"

        if name == "nt":
            run(f'tdp.exe {p} {q} {simulation_index} "{file_root}"', shell=True)
        else:
            run(f'./tdp {p} {q} {simulation_index} "{file_root}"', shell=True)


if __name__ == '__main__':
    set_start_method('spawn')
    simulation_name = "tdp"
    parameters = [0.7, 0]
    num_simulations = 24
    
    makedirs("temp", exist_ok=True)
    makedirs("outputs", exist_ok=True)

    file_root = ""
    if simulation_name == "tdp":
        system(f"gcc tdp.c -o tdp")  

    with Pool(num_simulations) as p:
        p.starmap(process, [(simulation_name, i, parameters) for i in range(num_simulations)])

    analysis(simulation_name, num_simulations, parameters)
    grapher(simulation_name, parameters)