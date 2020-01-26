class Humano:
    def __init__(self, simbolo):
        self.simbolo = simbolo

    def tomarAccion(self, env):
            while True:
                # break if we make a legal move
                move = int(input("Introduce las coordenadas i,j de tu siguiente movimiento [1-9]: "))

                if move == 1:
                    posicion = (0,0)
                elif move == 2:
                    posicion = (0,1)
                elif move == 3:
                    posicion = (0,2)
                elif move == 4:
                    posicion = (1,0)
                elif move == 5:
                    posicion = (1,1)
                elif move == 6:
                    posicion = (1,2)
                elif move == 7:
                    posicion = (2,0)
                elif move == 8:
                    posicion = (2,1)
                elif move == 9:
                    posicion = (2,2)

                i = int(posicion[0]) # X
                j = int(posicion[1]) # Y

                if env.estaLibre(i, j):
                    env.tablero[i,j] = self.simbolo
                    break

    def actualizacion(self, env):
        pass

    def añadir_estado_al_historial(self, s):
        pass