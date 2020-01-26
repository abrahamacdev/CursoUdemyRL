# From the course: Bayesin Machine Learning in Python: A/B Testing
# https://deeplearningcourses.com/c/bayesian-machine-learning-in-python-ab-testing
# https://www.udemy.com/bayesian-machine-learning-in-python-ab-testing
from __future__ import print_function, division
from builtins import range
# Note: you may need to update your version of future
# sudo pip install -U future

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

show = [0, 5, 10, 25, 50, 100, 200, 300, 500, 700, 1000, 1500]
vecesATirarMoneda = 1500

tope = 100 + 1


def plot(nVecesCruz, nVecesCara, trial, vecesQueSaleCara, t):
    global tope

    x = np.linspace(0, 1, 200) # Creamos un vector de 200 elementos con valores lineales con rango [0-1]
    y = beta.pdf(x, nVecesCruz, nVecesCara) # Creamos los valores de "y" usando la "Función de densidad de probabilidad"
    mean = float(nVecesCruz) / (nVecesCruz + nVecesCara)

    if tope == trial:
        print("y = " + str(np.array_str(y,precision=2,suppress_small=True)))
        print("Nº de veces que ha salido cara = " + str(nVecesCara))
        print("Nº de veces que ha salido cruz = " + str(nVecesCruz))
        print("Media estimada de que ganemos (salga cruz) = " + str(mean))
        print("Valor máx para el eje \"y\" " + str(np.amax(y)) + " ( posicion en el array " + str(np.argmax(y)) +", nº total de elementos = " + str(len(y)) + " )")
        fig_size = np.zeros(2)

        # Cambiamos el tamaño de la ventana
        fig_size[0] = 8
        fig_size[1] = 5

        plt.rcParams["figure.figsize"] = fig_size
        plt.plot(x,y)
        plt.xlabel("Densidad de probabilidad")
        plt.title("Distribución después de %s intentos, media real = %.1f, media estimada = %.2f" % (trial, vecesQueSaleCara, mean))
        plt.show()

    plt.plot(x, y)
    plt.plot(x, y)
    plt.title("Distributions after %s trials, true rate = %.1f, mean = %.2f" % (trial, vecesQueSaleCara, mean))
    plt.xlabel("Densidad de probabilidad")

    plt.savefig('C:/Users/Abraham/Documents/Github/LazyProgrammers/machine_learning_examples/rl/Abraham/_4_Bayesian_Thompson_Sampling/' + "iteracion" + str(trial))
    plt.close()
    #plt.show()

if __name__ == "__main__":
    vecesQueSaleCara = 0.50 # Realmente es 51%

    # Valores previos(priors)
    nVecesCruz = 1 # Nº de veces que ha estado por debajo de la media / Nº veces que ha salido NO
    nVecesCara = 1 # Nº de veces que ha estado por encima de la media / Nº veces que ha salido SI


    for t in range(vecesATirarMoneda + 1):
        resultado_lanzamiento_moneda = (np.random.random() < vecesQueSaleCara) # Si no sale cara
        if resultado_lanzamiento_moneda:
            nVecesCruz+= 1
        else:
            nVecesCara += 1

        if t in show:
            plot(nVecesCruz, nVecesCara, t+1, vecesQueSaleCara, t)

