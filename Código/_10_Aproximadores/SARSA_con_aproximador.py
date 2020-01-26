from Abraham.Código._7_DP import Grid
from Abraham.Código._7_DP.Grid import posiblesAccionesBasicas
from Abraham.Código._7_DP.iteracion_del_valor import mostrar_politica,mostrar_valores
from Abraham.Código._8_MonteCarlo.MonteCarlo_MejoraPoliticaNoES import MaxQ
import numpy as np
import matplotlib.pyplot as plt

GAMMA = 0.9
ALPHA = 0.1
EPS = 0.5

def accionRandom(a, eps = EPS):

    p = np.random.random()

    if p < (1 - eps):
        return a
    else:
        return np.random.choice(posiblesAccionesBasicas)



class Modelo:

    def __init__(self, grid):
        self.theta = np.random.randn(25) / np.sqrt(25) # Inicializamos los valores de #theta
        self.grid = grid
        pass

    def sa2x(self,s,a):
        return np.array([
            s[0] - 1 if a == 'U' else 0,
            s[1] - 1.5 if a == 'U' else 0,
            (s[0] * s[1] - 3) / 3 if a == 'U' else 0,
            (s[0] * s[0] - 2) / 2 if a == 'U' else 0,
            (s[1] * s[1] - 4.5) / 4.5 if a == 'U' else 0,
            1 if a == 'U' else 0,
            s[0] - 1 if a == 'D' else 0,
            s[1] - 1.5 if a == 'D' else 0,
            (s[0] * s[1] - 3) / 3 if a == 'D' else 0,
            (s[0] * s[0] - 2) / 2 if a == 'D' else 0,
            (s[1] * s[1] - 4.5) / 4.5 if a == 'D' else 0,
            1 if a == 'D' else 0,
            s[0] - 1 if a == 'L' else 0,
            s[1] - 1.5 if a == 'L' else 0,
            (s[0] * s[1] - 3) / 3 if a == 'L' else 0,
            (s[0] * s[0] - 2) / 2 if a == 'L' else 0,
            (s[1] * s[1] - 4.5) / 4.5 if a == 'L' else 0,
            1 if a == 'L' else 0,
            s[0] - 1 if a == 'R' else 0,
            s[1] - 1.5 if a == 'R' else 0,
            (s[0] * s[1] - 3) / 3 if a == 'R' else 0,
            (s[0] * s[0] - 2) / 2 if a == 'R' else 0,
            (s[1] * s[1] - 4.5) / 4.5 if a == 'R' else 0,
            1 if a == 'R' else 0,
            1
        ])



    def grad(self,s,a):
        return self.sa2x(s,a)

    def predecir(self,s,a):
        x = self.sa2x(s,a)
        return self.theta.dot(x)

    def obtenerQs(self,s):
        Qs = {}
        for a in posiblesAccionesBasicas:
            Qs[a] = self.predecir(s,a)

        return Qs




if __name__ == "__main__":

    grid = Grid.grid_negativo(-0.1)
    modelo = Modelo(grid)

    deltas = []
    n = 20000
    t = 1.0
    for i in range(n):

        if i % 100 == 0:
            t += 0.01

        if i % 1000 == 0:
            print(i)

        alpha = ALPHA / t # Hacemos que alpha decaiga con el tiempo

        mayorCambio = 0

        s = (2,0)
        grid.set_estado(s)

        qs = modelo.obtenerQs(s)
        a = MaxQ(qs)[1]
        a = accionRandom(a, EPS/t)

        while not grid.game_over():
            r = grid.mover(a) # Recompensa otorgada al 'sa' anterior
            s2 = grid.estado_actual() # Estado actual

            thetaAntiguo = modelo.theta.copy()

            # Si es terminal, "y" solo será la recompensa final
            if grid.es_terminal(s2):
                #y = r
                modelo.theta += alpha * (r - modelo.predecir(s, a)) * modelo.grad(s, a)

            # Si no es terminal, "y" será el valor esperado de las futuras recompensas
            else:
                qs2 = modelo.obtenerQs(s2)
                a2 = MaxQ(qs2)[1]
                a2 = accionRandom(a2, EPS/t)

                modelo.theta += alpha * (r + GAMMA * modelo.predecir(s2, a2) - modelo.predecir(s, a)) * modelo.grad(s, a)
                #y = r + GAMMA * modelo.predecir(s2,a2)


                #y_hat = modelo.predecir(s, a) # y^
                #modelo.theta += alpha * (y - y_hat) * modelo.grad(s, a) # Actualizamos nuestros pesos

                s = s2
                a = a2

            mayorCambio = max(mayorCambio,np.abs(modelo.theta - thetaAntiguo).sum())

        deltas.append(mayorCambio)

    plt.plot(deltas)
    plt.show()

    # Guardamos la política
    politica = {}
    for s in grid.acciones:
        Qs = modelo.obtenerQs(s)
        v,a = MaxQ(Qs)
        politica[s] = a

    print("Política final")
    mostrar_politica(politica,grid)