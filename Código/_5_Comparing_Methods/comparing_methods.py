from Abraham._2_optimistic_initial_values.optimistic_initial_values import ejecutarExperimento as optimistic
from Abraham._3_ucb1.ucb1 import ejecutarExperimento as ucb1
from Abraham._4_Bayesian_Thompson_Sampling.bayesian import ejecutarExperimento as bayes
from Abraham._5_Comparing_Methods.decaying_epsilon import ejecutarExperimento as decayingEpsilons
from Abraham.Utils import utils

import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":

    m1 = 1.0
    m2 = 2.0
    m3 = 3.0
    nVeces = 10000

    epsResultados = decayingEpsilons(m1,m2,m3,nVeces)
    optimisticResultados = optimistic(m1,m2,m3,nVeces)
    ucb1Resultados = ucb1(m1,m2,m3,nVeces)
    bayesResultados = bayes(m1,m2,m3,nVeces)



    utils.cambiarTamanioPlot(5,15)
    plt.plot(np.ones(nVeces) * m1)
    plt.plot(np.ones(nVeces) * m2)
    plt.plot(np.ones(nVeces) * m3)
    plt.plot(epsResultados, label="Eps" , c='b')
    plt.plot(optimisticResultados, label="Optimistic Initial Value", c='r')
    plt.plot(ucb1Resultados, label="UCB1", c='m')
    plt.plot(bayesResultados, label="Bayes", c='g')
    plt.legend()
    plt.xlabel("Nº de iteraciones")
    plt.ylabel("Media Acumulada")
    plt.xscale('log')
    plt.show()