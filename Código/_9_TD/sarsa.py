import numpy as np
import matplotlib.pyplot as plt
from Abraham.Código._7_DP import Grid
from Abraham.Código._7_DP.iteracion_del_valor import mostrar_politica,mostrar_valores


EPS = 0.75
GAMMA = 0.95
ALPHA = 0.1

def MaxQ(Q_s):
    MaxV = float("-inf")
    MaxA = None

    for a,v in Q_s.items():
        if v > MaxV:
            MaxV = v
            MaxA = a
    return MaxV,MaxA

def accionRandom(a,grid = Grid.grid_estandar(), eps=EPS):

    p = np.random.random()

    if p < (1.0 - eps):
        return a
    else:
        return np.random.choice(grid.posiblesAccionesBasicas())


if __name__ == "__main__":

    grid = Grid.grid_negativo(-0.1)
    todos_estados = grid.todos_estados()

    Q = {}
    alpha_personal = {}

    for s in todos_estados:
        Q[s] = {}
        alpha_personal[s] = {}

        for a in grid.posiblesAccionesBasicas():
            Q[s][a] = 0
            alpha_personal[s][a] = 1.0


    t = 1.0
    deltas = []

    nEpisodios = 5000
    for episo in range(nEpisodios):

        if episo % 100 == 0:
            print("Episodio = %d" % (episo))

        s = (2,0)
        grid.set_estado(s)
        a = MaxQ(Q[s])[1]
        a = accionRandom(a,grid, eps=EPS/t) # 0.75 / x

        cambioMayor = 0
        while not grid.game_over():

            r = grid.mover(a)
            s2 = grid.estado_actual()
            a2 = MaxQ(Q[s2])[1]
            a2 = accionRandom(a2,grid,eps=EPS/t)

            alpha = ALPHA / alpha_personal[s][a]
            alpha_personal[s][a] += 0.005

            antigua_qsa = Q[s][a]
            Q[s][a] = Q[s][a] + alpha * (r + GAMMA * Q[s2][a2] - Q[s][a])

            cambioMayor = max(cambioMayor,np.abs(Q[s][a] - antigua_qsa))

            s = s2
            a = a2

        deltas.append(cambioMayor)
        t += 1

    plt.plot(deltas)
    plt.show()

    politica = {}
    V = {}

    for s in grid.acciones:
        v,a = MaxQ(Q[s])
        politica[s] = a
        V[s] = v

    print("Política final")
    mostrar_politica(politica,grid)

    print("Valor final")
    mostrar_valores(V,grid)
