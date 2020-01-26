import numpy as np
import matplotlib.pyplot as plt
from Abraham._1_comparing_epsilons.comparing_epsilons import ejecutarExperimento as ejecutarExperimentoConEps
from Abraham._2_optimistic_initial_values.optimistic_initial_values import ejecutarExperimento as ejecutarExperimentoOiv

class Bandido:

    def __init__(self, mediaReal):
        self.mediaReal = mediaReal
        self.mediaCalculada = 0
        self.cuentaElementos = 0

    def tirarDePalanca(self):
        return np.random.randn() + self.mediaReal

    # @param X -> Nuevo elemento a tener en cuenta
    def actualizarMedia(self,X):
        self.cuentaElementos += 1 #Sumamos un elemento
        self.mediaCalculada = (1.0-1.0/self.cuentaElementos) * self.mediaReal + (1.0/self.cuentaElementos) * X


# Realiza el calculo de la "banda superior de confianza"
def ucb(mediaCalculada, n, cuentaElementos):
    if (cuentaElementos == 0):
        return float('inf')
    X_ucb_j = mediaCalculada + np.sqrt(2*np.log(n) / cuentaElementos) # Valor de la banda superior para la #mediaCalculada pasada
    return X_ucb_j

def ejecutarExperimento(mediaReal1,mediaReal2,mediaReal3,nVeces):

    # Array que contiene nuestros 3 objetos @Bandido
    bandidos = [Bandido(mediaReal1),Bandido(mediaReal2),Bandido(mediaReal3)]

    datos = np.empty(nVeces)

    for i in range (0,nVeces):

        # Cogemos el valor máximo del UCB de entre los 3 posibles bandidos
        bandidoElegido = np.argmax([ucb(bandido.mediaCalculada,i+1,bandido.cuentaElementos) for bandido in bandidos])

        X = bandidos[bandidoElegido].tirarDePalanca() # Obtenemos un nuevo valor de nuestro bandido
        bandidos[bandidoElegido].actualizarMedia(X) # Le añadimos el nuevo valor a la media calculada

        datos[i] = X # Guardamos el valor

    # Media acumulada de los valores obtenidos de cada bandido
    mediaAcumulada = np.cumsum(datos) / (np.arange(nVeces) + 1)

    # Mostramos los valores de las medias reales en comparacion con los valores medios
    # obtenidos de los bandidos
    plt.plot(mediaAcumulada)
    plt.plot(np.ones(nVeces) * mediaReal1) # Vector de tamaño #nVeces con los valores de la #mediaReal1
    plt.plot(np.ones(nVeces) * mediaReal2) # Vector de tamaño #nVeces con los valores de la #mediaReal2
    plt.plot(np.ones(nVeces) * mediaReal3) # Vector de tamaño #nVeces con los valores de la #mediaReal3
    plt.xlabel("Número de iteraciones")
    plt.ylabel("Medias reales/acumulada")
    plt.xscale('log')
    plt.show()

    return mediaAcumulada

# Estamos llamando el script desde la consola de comandos
if __name__ == "__main__":

    eps_1 = ejecutarExperimentoConEps(1.0, 2.0, 3.0, 0.1, 10000)
    ucb1 = ejecutarExperimento(1.0, 2.0, 3.0, 10000)
    oiv = ejecutarExperimentoOiv(1.0, 2.0, 3.0, 10000)


    plt.plot(eps_1, label="Eps (0.1)")
    plt.plot(ucb1, label="UCB1")
    plt.plot(oiv, label="Optimal Initial Value")
    plt.xlabel("Número de iteraciones")
    plt.xscale('log')
    plt.ylabel("Media acumulada de cada bandido")
    plt.legend()
    plt.show()