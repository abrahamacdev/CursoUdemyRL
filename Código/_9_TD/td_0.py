import numpy as np
from Abraham.Código._7_DP import Grid
from Abraham.Código._7_DP.iteracion_del_valor import mostrar_valores,mostrar_politica

EPS = 0.3
GAMMA = 0.95
ALPHA = 0.01

def accionRandom(a,grid,eps = EPS):
    """
        Damos posibilidad a las demás acciones de
        ser elegidas
    """

    p = np.random.random()

    if p < (1 - eps):
        return a
    else:
        return np.random.choice(grid.posiblesAccionesBasicas())

def jugar(politica,grid):

    s = (2,0)
    grid.set_estado(s)
    a = politica[s]
    a = accionRandom(a,grid)
    estados_recompensas = [(s,0)]

    while not grid.game_over():
        r = grid.mover(a)
        s = grid.estado_actual()
        estados_recompensas.append((s,r))

        if s in grid.acciones:
            a = politica[s]
            a = accionRandom(a,grid)

    return estados_recompensas


if __name__ == "__main__":

    grid = Grid.grid_estandar()
    todos_estados = grid.todos_estados()

    politica = {
        (2, 0): 'U',
        (1, 0): 'U',
        (0, 0): 'R',
        (0, 1): 'R',
        (0, 2): 'R',
        (1, 2): 'R',
        (2, 1): 'R',
        (2, 2): 'R',
        (2, 3): 'U'
    }

    V = {}
    for s in todos_estados:
        V[s] = 0


    nEpiso = 2000

    for episo in range(nEpiso):

        estados_recompensas = jugar(politica,grid)

        for i in range(len(estados_recompensas) - 1):

            s,_ = estados_recompensas[i]
            s2,r = estados_recompensas[i+1]

            V[s] = V[s] + ALPHA * (r + GAMMA * V[s2] - V[s])


    print("Política Determinista")
    mostrar_politica(politica,grid)

    print("Valores finales")
    mostrar_valores(V,grid)