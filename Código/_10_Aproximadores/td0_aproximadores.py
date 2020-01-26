import numpy as np
import matplotlib.pyplot as plt
from Abraham.Código._7_DP import Grid
from Abraham.Código._7_DP.iteracion_del_valor import mostrar_valores, mostrar_politica

EPS = 0.1 # Probabilidad de escoger acción aleatoria
GAMMA = 0.9
ALPHA = 0.1

def accionRandom(a, grid, eps = EPS):

    """
        Si #p < #eps retornábamos la acción de la política,
        sino, la probabilidad restante era repartida entre todas las posibles acciones
    """
    p = np.random.random()

    if p < (1 - eps):
        return a
    else:
        return np.random.choice(grid.posiblesAccionesBasicas())

def jugar(politica,grid = Grid.grid_estandar()):

    s = (2,0) # No starter method
    grid.set_estado(s)

    acciones_recompensas = [(s,0)]

    while not grid.game_over():
        a = politica[s]
        a = accionRandom(a,grid)
        r = grid.mover(a)
        s = grid.estado_actual()
        acciones_recompensas.append((s,r))

    return acciones_recompensas

def predecir(x,theta):
     return theta.dot(x) # theta^T * x

def funcionCostos(x,y,theta):
    return y - predecir(x,theta) # (y - theta^T * x)

def StoX(S):
    return np.array([S[0] - 1, S[1] - 1.5, S[0] * S[1] - 3, 1]) # [filaNorm, columNorm, (fil*col)Norm, bias]


if __name__ == "__main__":

    grid = Grid.grid_negativo(-0.1)
    todosEstados = grid.todos_estados()

    politica = {
        (2, 0): 'U',
        (1, 0): 'U',
        (0, 0): 'R',
        (0, 1): 'R',
        (0, 2): 'R',
        (1, 2): 'R',
        (2, 1): 'R',
        (2, 2): 'R',
        (2, 3): 'U',
    }

    theta = np.random.rand(4) / 2 # Inicializamos los valores de Theta

    deltas = []

    n = 20000
    k = 1.0
    for i in range(1,n):

        cambioMayor = 0

        if i % 100 == 0:
            k += 0.5

        alpha = ALPHA / k

        estados_recompensas = jugar(politica,grid)

        for i in range(len(estados_recompensas)-1):
            thetaAntiguo = theta.copy()
            s, _ = estados_recompensas[i]
            s2, r = estados_recompensas[i+1]

            if grid.es_terminal(s2):
                V_real = r

            else:
                V_real = r + GAMMA * predecir(StoX(s2),theta) # Convertimos y^ usando nuestro aproximador

            x = StoX(s)
            V_hat = predecir(x,theta)

            theta += alpha * (V_real - V_hat) * x

            cambioMayor = max(cambioMayor,np.abs(thetaAntiguo - theta).sum())

        deltas.append(cambioMayor)

    plt.plot(deltas)
    plt.show(deltas)

    V = {}
    for s in politica:
        V[s] = predecir(StoX(s),theta)

    mostrar_valores(V,grid)
    mostrar_politica(politica,grid)