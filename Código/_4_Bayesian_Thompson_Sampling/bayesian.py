import numpy as np
import matplotlib.pyplot as plt

class BandidoBayesiano:

    def __init__(self, mediaReal):
        self.mediaReal = mediaReal

        # parameters for mu - prior is N(0,1)
        self.mediaCalculada = 0
        self.lambda_ = 1
        self.sum_x = 0  # for convenience

        self.tau = 1 # tau es constante

    # Devuelve un ejemplo real
    def tirarDePalanca(self):
        return np.random.randn() + self.mediaReal

    # Devuelve una estimación de nuestro algoritmo
    def predecirValor(self):
        return np.random.randn() / np.sqrt(self.lambda_) + self.mediaCalculada

    # @param X -> Nuevo elemento a tener en cuenta
    def actualizarMedia(self,X):
        self.lambda_ += self.tau
        self.sum_x += X
        self.mediaCalculada = self.tau * self.sum_x / self.lambda_


def mostrarBandidoBayesiano(bandidoBayesiano):
    print("Media real = " + str(bandidoBayesiano.mediaReal))
    print("Media calculada/acumulada = " + str(bandidoBayesiano.mediaCalculada))
    print("Lambda = " + str(bandidoBayesiano.lambda_))
    print("Suma de x (contador) = " + str(bandidoBayesiano.sum_x))
    print("Tau = " + str(bandidoBayesiano.tau))
    print("Predicción actual = " + str(bandidoBayesiano.predecirValor()))
    print("----------")

def ejecutarExperimento(mediaReal1, mediaReal2, mediaReal3, nVeces):

    # Array que contiene nuestros 3 objetos @Bandido
    bandidos = [BandidoBayesiano(mediaReal1), BandidoBayesiano(mediaReal2), BandidoBayesiano(mediaReal3)]

    datos = np.empty(nVeces)

    for i in range(0, nVeces):

        aElegir = np.argmax([bandido.predecirValor() for bandido in bandidos]) # Cogemos el valor máximo de entre los 3 posibles bandidos
        X = bandidos[aElegir].tirarDePalanca()  # Obtenemos un nuevo valor de nuestro bandido
        bandidos[aElegir].actualizarMedia(X)  # Le añadimos el nuevo valor a la media calculada

        datos[i] = X  # Guardamos el valor

        #mostrarBandidoBayesiano(bandidos[aElegir])


    # Media acumulada de los valores obtenidos de cada bandido
    mediaAcumulada = np.cumsum(datos) / (np.arange(nVeces) + 1)

    return mediaAcumulada


if __name__ == "__main__":

    m1 = 1.0
    m2 = 2.0
    m3 = 3.0

    bayes = ejecutarExperimento(m1, m2, m3, 10000)

    plt.plot(bayes, label='bayesian')
    plt.legend()
    plt.xscale('log')
    plt.show()

    plt.plot(bayes, label='bayesian')
    plt.legend()
    plt.show()