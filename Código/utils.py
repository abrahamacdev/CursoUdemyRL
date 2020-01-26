import matplotlib.pyplot as plt

def cambiarTamanioPlot(alto, ancho):
    fig_size = [None] * 2
    fig_size[0] = ancho
    fig_size[1] = alto

    plt.rcParams["figure.figsize"] = fig_size