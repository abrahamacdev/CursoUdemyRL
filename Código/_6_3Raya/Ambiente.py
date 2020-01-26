import numpy as np

LENGTH = 3

class Ambiente:
    def __init__(self, espectar=False):
        self.cantOpciones = 3 # 0 -> Vacío, -1 -> Jug1, 1 -> Jug2
        self.x = 1 # 1 -> Jug2
        self.o = -1 # -1 -> Jug1
        self.tablero = np.zeros((LENGTH, LENGTH)) # Tamaño del tablero
        self.tamañoTablero = 9 # Dado que es 3 en raya
        self.cantEstados = self.cantOpciones ** self.tamañoTablero # 3^9
        self.ganador = None
        self.terminado = False
        self.espectar = espectar # Modo espectador

    """ 
        Determinamos si el juego ha terminado comprobando las filas, columnas 
        y diagonales.
        * Si el tablero está completo y tiene estados extraños (todo 0's),
          indicará que el juego no ha acabado ni habrá ganador
    """
    def gameOver(self, forzar_recalculo = False):

        """
            La función podría ser llamada varias veces
            una vez halla acabado la partida, no queremos comprobar
            la tabla toodo el rato.
        """
        if not forzar_recalculo and self.terminado:
            return self.terminado

        # Comprobamos las filas
        for i in range(LENGTH):
            # Recorremos el número de jugadores que tenemos
            for jugador in (self.x, self.o):
                if self.tablero[i].sum() == jugador * LENGTH:
                    self.ganador = jugador
                    self.terminado = True
                    return True

        # Comprobamos las columnas
        for j in range(self.cantOpciones):
            # Recorremos los valores tomados por cada jugador
            for jugador in (self.x, self.o):
                if self.tablero[:, j].sum() == jugador * LENGTH:
                    self.ganador = jugador
                    self.terminado = True
                    return True

        # Comprobamos los diagonales
        for jugador in (self.x, self.o):

            # superior-izquierda-> inferior-derecha
            if self.tablero.trace() == jugador * LENGTH:
                self.ganador = jugador
                self.terminado = True
                return True

            # superior-derecha -> inferior-izquierda
            if np.fliplr(self.tablero).trace() == jugador * LENGTH:
                self.ganador = jugador
                self.terminado = True
                return True

        #Comprobamos si hay empate
        if np.all((self.tablero == 0) == False):
        #if np.all(self.tablero != 0):
            # no tenemos ningún ganador
            self.ganador = None
            self.terminado = True
            return True

        # El juego aún no ha acabado
        self.ganador = None
        return False

    def obtenerEstado(self):
        # retorna el estado actual representado como un número
        # ese número solo podrá tomar valores desde 0..S-1 (Todos los posibles estados)
        # S.length = 3^(tamañoTablero) (Cada celda solo puede contener 3 valores: -1,0,1)
        # * algunos estados no son posibles. Ej: Todas las celdas valen 0, ignoramos estos casos
        # ** pasamos un número a otro que estará en base-3
        numeroFinal = 0
        posicion = 0
        for i in range(self.cantOpciones):
            for j in range(self.cantOpciones):
                if self.tablero[i, j] == 0:
                    v = 0
                elif self.tablero[i, j] == self.x:
                    v = 1
                elif self.tablero[i, j] == self.o:
                    v = 2

                #numeroFinal += v * (3 ** posicion) # pasamos el número a base 3
                numeroFinal += (3 ** posicion) * v
                posicion += 1
        return numeroFinal

    def estaOcupada(self,x,y):
        # comprobamos si una posicion esta ocupada
        return self.tablero[x,y] != 0

    def estaLibre(self,x,y):
        # comprobamos si una posicion esta libre
        return self.tablero[x,y] == 0

    def recompensa(self,jugador):
        # otorgamos la recompensa al jugador
        recompensa = 0
        if (self.terminado):
            recompensa = 1 if self.ganador == jugador else 0

        return recompensa

    def dibujarTablero(self):
        for i in range(self.cantOpciones):
            print("----------")
            for j in range(self.cantOpciones):
                print(" ", end="")
                if self.tablero[i,j] == self.x:
                    print("X ", end="")
                elif self.tablero[i,j] == self.o:
                    print("O ", end="")
                else:
                    print("  ", end="")
            print("")
        print("----------")