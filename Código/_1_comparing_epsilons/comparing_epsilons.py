import numpy as np
import matplotlib.pyplot as plt


class Bandido:

    def __init__(self, mediaReal):
        self.mediaReal = mediaReal
        self.numElementos = 0
        self.mediaAcumulada= 0

    def tirarDePalanca(self):
        return np.random.randn() + self.mediaReal

    # @param X -> Nuevo elemento a tener en cuenta
    def actualizarMedia(self,X):
        self.numElementos += 1 #Sumamos un elemento
        self.mediaAcumulada = (1-1.0/self.numElementos) * self.mediaAcumulada + (1.0/self.numElementos) * X



def ejecutarExperimento(mediaReal1,mediaReal2,mediaReal3,eps,nVeces):

    # Array que contiene nuestros 3 objetos @Bandido
    bandidos = [Bandido(mediaReal1),Bandido(mediaReal2),Bandido(mediaReal3)]

    datos = np.empty(nVeces)

    for i in range (0,nVeces):

        random = np.random.rand() # Número aleatorio para posible exploracion
        aElegir = 0 # Bandido a elegir de nuestro array
        if(random < eps):
            aElegir= np.random.choice(3)  # Elegimos de manera aleatoria uno de nuestros 3 posibles bandidos
        else:
            # Cogemos el valor máximo de entre los 3 posibles bandidos
            aElegir = np.argmax([bandido.mediaAcumulada for bandido in bandidos])

        X = bandidos[aElegir].tirarDePalanca() # Obtenemos un nuevo valor de nuestro bandido
        bandidos[aElegir].actualizarMedia(X) # Le añadimos el nuevo valor a la media calculada
        datos[i] = X # Guardamos el valor

    # Media acumulada de los valores obtenidos de cada bandido
    mediaAcumulada = np.cumsum(datos) / (np.arange(nVeces) + 1) # Ej: [2,2,4,8] / [0,1,2,3] + 1

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

    eps_1 = ejecutarExperimento(1.0,2.0,3.0,0.1,10000)
    eps_05 = ejecutarExperimento(1.0, 2.0, 3.0, 0.05, 10000)
    eps_01 = ejecutarExperimento(1.0, 2.0, 3.0, 0.01, 10000)

    plt.plot(eps_1, label="eps = 0.1")
    plt.plot(eps_05, label="eps = 0.05")
    plt.plot(eps_01, label="eps = 0.01")
    plt.xlabel("Número de iteraciones")
    plt.xscale('log')
    plt.ylabel("Media acumulada de cada bandido")
    plt.legend()
    plt.show()