from Abraham._6_3Raya.Ambiente import Ambiente
import numpy as np

class Agente:
    def __init__(self,alpha=0.5,eps=0.1):
        self.alpha = alpha # tasa de aprendizaje
        self.eps = eps # probabilidad de escoger una acción aleatoria
        self.historial = [] # matriz con las acciones realizadas

    def setSimbolo(self,simbolo):
        self.simbolo = simbolo  # símbolo para el juego (-1->O, 1->X)

    def setValue(self,value):
        self.value = value # matriz con las funciones de valor

    def resetearHistorial(self):
        self.historial = []



    def tomarAccion(self, env):
        random = np.random.rand()
        mejorEstado = None

        # Tomamos una acción aleatoria
        if random < self.eps:

            posibles_movimientos = []
            for i in range(env.cantOpciones):
                for j in range(env.cantOpciones):
                    if env.estaLibre(i,j):
                        posibles_movimientos.append((i,j))
            eleccion = np.random.choice(len(posibles_movimientos)) # elegimos la acción a llevar a cabo
            siguienteMovimiento = posibles_movimientos[eleccion] # guardamos unicamente esa accion

        # Tomamos una acción basada en el conocimiento
        # Escogemos la mejor accion basada en los valores actuales de los estados
        else:
            # recorremos todos los posibles movimientos, obtenemos sus valores
            # guardamos aquel con mayor valor
            mejorValor = -1
            siguienteMovimiento = None

            """ Recorremos el tablero """
            for i in range(env.cantOpciones):
                for j in range(env.cantOpciones):
                    if env.estaLibre(i, j):
                        env.tablero[i,j] = self.simbolo # que pasaría si hiciesemos este movimiento
                        estado = env.obtenerEstado() # obtenemos un número en base 3
                        env.tablero[i, j] = 0 # dejamos el tablero como estaba
                        if self.value[estado] > mejorValor:
                            mejorValor = self.value[estado]
                            mejorEstado = estado
                            siguienteMovimiento = (i,j)

        env.tablero[siguienteMovimiento[0], siguienteMovimiento[1]] = self.simbolo

    def añadir_estado_al_historial(self, estado):
        """
            Añadimos el estado al historial cada vez que cualquiera
            de los dos jugadores haga un movimiento
            estado = env.obtenerEstado()
        """
        self.historial.append(estado)

    def actualizacion(self,env):
        """
            Tenemos que recorrer el historial al revés, de forma que
            V(estado) =  V(estado) + alpha * (V(estado_siguiente) - V(estado))
            donde V(estado_siguiente) = recompensa, si es el estado mas actual

            * Solo haremos esto al acabar una partida
        """
        recompensa = env.recompensa(self.simbolo)
        ultValorObtenido = recompensa # Recompensa ocnseguida en la última partida
        for prev in reversed(self.historial):
            valor = self.value[prev] + self.alpha * (ultValorObtenido - self.value[prev])
            self.value[prev] = valor # Actualizamos el valor del último V()
            ultValorObtenido = valor

        self.resetearHistorial()