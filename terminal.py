from multiprocessing import set_start_method, Pool, cpu_count
from os import makedirs, name, system
from subprocess import run

from analysis import analysis
from grapher import grapher
from utils import *


def child_process(simulation_name, simulation_index, parameters):
    if simulation_name == "tdp":
        p = parameters[0]
        q = parameters[1]
        file_root = f"temp/tdp_{str(p).replace('.', 'p')}_{str(q).replace('.', 'q')}_{simulation_index}_"

        if name == "nt":
            run(f'tdp.exe {p} {q} {simulation_index} "{file_root}"', shell=True)
        else:
            run(f'./tdp {p} {q} {simulation_index} "{file_root}"', shell=True)


def run_simulation(simulation_name, parameter_values):
    if simulation_name == "tdp":
        system(f"gcc tdp.c -o tdp") 

    for parameters in parameter_values:
        delete_files_in_dir("temp/")
         
        with Pool(num_simulations) as p:
            p.starmap(child_process, [(simulation_name, i, parameters) for i in range(num_simulations)])

        analysis(simulation_name, num_simulations, parameters)
        grapher(simulation_name, parameters)


if __name__ == '__main__':
    makedirs("temp", exist_ok=True)
    makedirs("outputs", exist_ok=True)
    set_start_method('spawn')
    num_simulations = cpu_count() - 1

    simulation_name = "tdp"
    # parameter_values = [
    #     [0.65, 0],
    #     [0.7, 0],
    #     [0.72, 0],
    # ]
    parameter_values = [
        [0.51, 0.5],
        [0.535, 0.5],
        [0.55, 0.5]
    ]
    
    run_simulation(simulation_name, parameter_values)