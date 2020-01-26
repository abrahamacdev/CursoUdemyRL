import numpy as np
import matplotlib.pyplot as plt

# El bandido servirá simplemente para darnos valores
class Bandido:

    def __init__(self, mediaReal):
        self.mediaReal = mediaReal
        self.numElementos = 0
        self.mediaAcumulada = 0

    def tirarPalanca(self):
        return np.random.randn() + self.mediaReal

    def actualizarMedia(self, nuevoValor):
        self.numElementos += 1
        self.mediaAcumulada = (1.0 - 1.0/self.numElementos) * self.mediaAcumulada + 1.0/self.numElementos * nuevoValor

def ejecutarExperimentoArray(bandidos,nVeces):

    # Iremos guardando los valores elegidos en cada iteracion
    datos = np.zeros(nVeces)

    y = len(bandidos)
    x = 0

    for i in range(0,nVeces):
        eps = 1.0/(i+1) # Hacemos que eps decaiga

        bandidoElegido = 0

        if (np.random.rand() < eps ):
            bandidoElegido = np.random.choice(len(bandidos)) # Elegimos un @Bandido de forma aleatoria
        else:
            bandidoElegido = np.argmax([bandido.mediaAcumulada for bandido in bandidos]) # Elegimos el bandido con mejor media acumulada

        x = bandidos[bandidoElegido].tirarPalanca() # Tiramos de la palanca de uno de los bandidos
        bandidos[bandidoElegido].actualizarMedia(x) # Actualizamos la media del @Bandido

        datos[i] = x

    mediaAcumulada = np.cumsum(datos) / (np.arange(nVeces) + 1) # Ej: [2,2,4,8] / [0,1,2,3] + 1

    for i in range(0,len(bandidos)):
        plt.plot(np.ones(nVeces) * bandidos[i].mediaReal) # Por cada #mediaReal de cada @Bandido, hacemos un vector

    plt.plot(mediaAcumulada)
    plt.xlabel("Nº de iteraciones")
    plt.ylabel("Medias reales(lineales) | Media acumulada(no lineal)")
    plt.xscale('log')
    plt.show()

def ejecutarExperimento(m1,m2,m3,nVeces):

    # Array con los bandidos
    bandidos = [Bandido(m1),Bandido(m2),Bandido(m3)]

    # Iremos guardando los valores elegidos en cada iteracion
    datos = np.zeros(nVeces)

    for i in range(0, nVeces):
        eps = 1.0 / (i + 1)  # Hacemos que eps decaiga

        bandidoElegido = 0

        if (np.random.rand() < eps):
            bandidoElegido = np.random.choice(len(bandidos))  # Elegimos un @Bandido de forma aleatoria
        else:
            bandidoElegido = np.argmax(
                [bandido.mediaAcumulada for bandido in bandidos])  # Elegimos el bandido con mejor media acumulada

        x = bandidos[bandidoElegido].tirarPalanca()  # Tiramos de la palanca de uno de los bandidos
        bandidos[bandidoElegido].actualizarMedia(x)  # Actualizamos la media del @Bandido

        datos[i] = x

    mediaAcumulada = np.cumsum(datos) / (np.arange(nVeces) + 1)  # Ej: [2,2,4,8] / [0,1,2,3] + 1

    for i in range(0, len(bandidos)):
        plt.plot(np.ones(nVeces) * bandidos[i].mediaReal)  # Por cada #mediaReal de cada @Bandido, hacemos un vector

    return mediaAcumulada

if __name__ == "__main__":

    m1 = 1.0
    m2 = 2.0
    m3 = 3.0
    nVeces = 10000

    bandidos = [Bandido(m1),Bandido(m2),Bandido(m3)]
    mediaAcumulada = ejecutarExperimentoArray(bandidos, nVeces)

    plt.plot(mediaAcumulada)
    plt.xlabel("Nº de iteraciones")
    plt.ylabel("Medias reales(lineales) | Media acumulada(no lineal)")
    plt.xscale('log')
    plt.show()

