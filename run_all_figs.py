from fig1 import fig1
from fig2_exp import fig2_exp
from fig2 import fig2
from fig3 import fig3
from fig4 import fig4
from fig5 import fig5
from fig6 import fig6
from fig7 import fig7


if __name__ == '__main__':
    main_fig = False
    model_dataset = "256x256_64"
    scanlon = "8_24"
    null_dataset = "256x256_64"
    
    fig1(model_dataset, scanlon, null_dataset, main_fig)
    fig2_exp(model_dataset, scanlon, null_dataset, main_fig)
    fig2(model_dataset, scanlon, null_dataset, main_fig)
    fig3(model_dataset, scanlon, null_dataset, main_fig)
    fig4(model_dataset, scanlon, null_dataset, main_fig)
    fig5(model_dataset, scanlon, null_dataset, main_fig, 50)
    fig5(model_dataset, scanlon, null_dataset, main_fig, 100)
    fig6(model_dataset, scanlon, null_dataset, main_fig)
    fig7(model_dataset, scanlon, null_dataset, main_fig)