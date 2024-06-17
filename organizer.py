from os import listdir, makedirs
from shutil import move


def organize(simulation_name, parameter_values):
    if simulation_name == "tdp":
        for parameters in parameter_values:
            p = parameters[0]
            q = parameters[1]
            prefix = f"tdp_{str(p).replace('.', 'p')}_{str(q).replace('.', 'q')}"
            makedirs(output_path + prefix, exist_ok=True)

            for output_file in listdir(output_path):
                if output_file.startswith(prefix):
                    print(f"Moving {output_file} to {prefix}")
                    move(output_path + output_file, output_path + prefix)



if __name__ == '__main__':
    output_path = "outputs/"

    simulation_name = "tdp"
    parameter_values = [
        [0.65, 0],
        [0.7, 0],
        [0.72, 0],
    ]

    organize(simulation_name, parameter_values)