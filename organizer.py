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
                    move(output_path + output_file, output_path + prefix)
    elif simulation_name == "scanlon":
        for parameters in parameter_values:
            rainfall = parameters[0]
            prefix = f"scanlon_{str(rainfall).replace('.', 'p')}"
            makedirs(output_path + prefix, exist_ok=True)

            for output_file in listdir(output_path):
                if output_file.startswith(prefix):
                    move(output_path + output_file, output_path + prefix)
    elif simulation_name == "null":
        for parameters in parameter_values:
            f = parameters[0]
            prefix = f"null_{str(f).replace('.', 'p')}"
            makedirs(output_path + prefix, exist_ok=True)

            for output_file in listdir(output_path):
                if output_file.startswith(prefix):
                    move(output_path + output_file, output_path + prefix)



if __name__ == '__main__':
    output_path = "outputs/"

    # simulation_name = "tdp"
    # parameter_values = [
    #     [0.65, 0],
    #     [0.7, 0],
    #     [0.72, 0],
    # ]

    simulation_name = "tdp"
    parameter_values = [
        [0.51, 0.5],
        [0.535, 0.5],
        [0.55, 0.5]
    ]

    # simulation_name = "tdp"
    # parameter_values = [
    #     [0.585, 0.25],
    #     [0.62, 0.25],
    #     [0.645, 0.25]
    # ]

    # simulation_name = "tdp"
    # parameter_values = [
    #     [0.405, 0.75],
    #     [0.41, 0.75],
    #     [0.42, 0.75]
    # ]

    # simulation_name = "scanlon"
    # parameter_values = [
    #     [500],
    #     [770],
    #     [850]
    # ]

    # simulation_name = "null"
    # parameter_values = [
    #     [0.25],
    #     [0.26],
    #     [0.27],
    #     [0.45],
    #     [0.48],
    #     [0.49],
    #     [0.53],
    #     [0.54],
    #     [0.56]
    # ]

    # simulation_name = "null"
    # parameter_values = [
    #     [0.24],
    #     [0.44],
    #     [0.23],
    #     [0.38],
    #     [0.52]
    # ]

    # simulation_name = "tdp"
    # parameter_values = [
    #     [0.618, 0],
    #     [0.62, 0],
    #     [0.625, 0],
    #     [0.63, 0],
    #     [0.64, 0],
    #     [0.68, 0],
    #     [0.74, 0]
    # ]

    # simulation_name = "tdp"
    # parameter_values = [
    #     [0.5, 0.5],
    #     [0.505, 0.5],
    #     [0.52, 0.5],
    #     [0.53, 0.5],
    #     [0.54, 0.5],
    #     [0.56, 0.5]
    # ]

    # simulation_name = "scanlon"
    # parameter_values = [
    #     [300],
    #     [400],
    #     [600],
    #     [700],
    #     [800],
    #     [900]
    # ]

    # simulation_name = "tdp"
    # parameter_values = [
    #     [0.282, 0.92],
    #     [0.2825, 0.92],
    #     [0.283, 0.92],
    #     [0.2835, 0.92],
    #     [0.284, 0.92],
    #     [0.2845, 0.92],
    #     [0.285, 0.92]
    # ]

    # simulation_name = "tdp"
    # parameter_values = [
    #     [0.65, 0],
    #     [0.7, 0],
    #     [0.51, 0.5],
    #     [0.535, 0.5]
    # ]

    organize(simulation_name, parameter_values)