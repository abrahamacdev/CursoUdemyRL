import numpy as np
import matplotlib.pyplot as plt
from Abraham._1_comparing_epsilons.comparing_epsilons import ejecutarExperimento as ejecutarExperimentoConEps

class Bandido:

    def __init__(self, mediaReal, limiteSuperior):
        self.mediaReal = mediaReal
        self.mediaCalculada = limiteSuperior # Comenzamos estableciendo nuestra #mediaCalculada con el valor del #límiteSuperior
        self.cuentaElementos = 1 # Ya hemos añadido el primer valor

    def tirarDePalanca(self):
        return np.random.randn() + self.mediaReal

    # @param X -> Nuevo elemento a tener en cuenta
    def actualizarMedia(self,X):
        self.cuentaElementos += 1 #Sumamos un elemento
        self.mediaCalculada = (1-1.0/self.cuentaElementos) * self.mediaReal + (1.0/self.cuentaElementos) * X



def ejecutarExperimento(mediaReal1,mediaReal2,mediaReal3,nVeces,limiteSuperior = 10):

    # Array que contiene nuestros 3 objetos @Bandido
    bandidos = [Bandido(mediaReal1, limiteSuperior),Bandido(mediaReal2, limiteSuperior),Bandido(mediaReal3, limiteSuperior)]

    datos = np.empty(nVeces)

    for i in range (0,nVeces):

        # Cogemos el valor máximo de entre los 3 posibles bandidos
        aElegir = np.argmax([bandido.mediaCalculada for bandido in bandidos])

        X = bandidos[aElegir].tirarDePalanca() # Obtenemos un nuevo valor de nuestro bandido
        bandidos[aElegir].actualizarMedia(X) # Le añadimos el nuevo valor a la media calculada

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
    oiv = ejecutarExperimento(1.0, 2.0, 3.0, 10000)


    plt.plot(eps_1, label="eps = 0.1")
    plt.plot(oiv, label="oiv")
    plt.xlabel("Número de iteraciones")
    plt.xscale('log')
    plt.ylabel("Media acumulada de cada bandido")
    plt.legend()
    plt.show()



