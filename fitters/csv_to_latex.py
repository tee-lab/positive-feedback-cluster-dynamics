from os import path
import pandas as pd


if __name__ == '__main__':
    folder_name = "scanlon_cd"
    file_name = "scanlon_cd.csv"
    path_to_file = path.join(path.dirname(__file__), folder_name, file_name)

    data = pd.read_csv(path_to_file)
    num_rows = data.shape[0]
    cols = [data["p"], data["PL BIC"], data["TPL BIC"], data["Exp BIC"], data["PL expo"], data["TPL expo"], data["TPL trunc"], data["Exp trunc"]]
    precisions = [0, 0, 0, 0, 2, 2, 2, 2]
    
    latex_string = ""

    for row in range(num_rows):
        latex_line = ""
        
        for i, col in enumerate(cols):
            if precisions[i] == 0:
                latex_line += f"{col.iloc[row]:.0f} & "
            elif precisions[i] == 3:
                latex_line += f"{col.iloc[row]:.3f} & "
            elif precisions[i] == 2:
                latex_line += f"{col.iloc[row]:.2f} & "
        
        latex_line = latex_line[:-2]
        latex_string += latex_line + "\\\\ \n"

    print(latex_string)