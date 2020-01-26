import numpy as np
import matplotlib.pyplot as plt

from Abraham.Código._7_DP.iteracion_del_valor import mostrar_valores, mostrar_politica
from Abraham.Código._7_DP import Grid

EPS = 0.1
GAMMA = 0.99
ALPHA = 0.001

def aleatoriedadAcciones(a, grid, eps = EPS):
    p = np.random.random()

    # Probabilidad de elegir la acción de la política
    if p < (1.0 - eps):
        return a

    else:
        return np.random.choice(grid.posiblesAccionesBasicas())

def generarEjemplo(politica,grid):

    # Comenzaremos siempre desde el mismo lado
    s = (2,0)
    grid.set_estado(s)

    # Cogemos la primera acción según la política
    a = aleatoriedadAcciones(politica[s],grid)

    estados_acciones_recompensas = [(s,a,0)]

    """ Ejecutamos la simulación hasta que acabemos"""
    acabado = False
    while not acabado:
        r = grid.mover(a)
        s = grid.estado_actual()

        # El estado actual es terminal, no seteamos accion
        if grid.game_over():
            estados_acciones_recompensas.append((s,None,r))
            acabado = True

        # El estado actual no es terminal, toddo normal
        else:
            a = aleatoriedadAcciones(politica[s],grid)
            estados_acciones_recompensas.append((s,a,r))

    """ Calculamos los retornos """
    G = 0
    estados_acciones_retornos = []
    primero = True

    for s,a,r in reversed(estados_acciones_recompensas):
        # El estado terminal es ignorado
        if primero:
            primero = False

        # Estado normal, añadimos los retornos
        else:
            estados_acciones_retornos.append((s,a,G))
        G = r + GAMMA * G


    estados_acciones_retornos.reverse()
    return estados_acciones_retornos

def convertirS_X(s):
    """
    0 -> Media de las filas (2, la nº 0 no cuenta)
    1 -> Media de las columnas (3, la nº 0 no cuenta)
    2 -> Media del número de celdas quitando la columna 0 y la fila 0 (6 celdas en total)
    4 -> Bias
    """
    return np.array([s[0] - 1, s[1] - 1.5, s[0] * s[1] - 3, 1])

def MaxQsa(Qs):
    MaxV = float('-inf')
    MaxA = None

    for k,v in Qs.items():
        if v > MaxV:
            MaxV = v
            MaxA = k

    return (MaxA,MaxV)


if __name__ == "__main__":

    grid = Grid.grid_negativo(-0.10)
    estados = grid.todos_estados()

    # Esta vez serán nuestros pesos los que nos guíen
    theta = np.random.randn(4) / 2

    politica = {
        (2, 0): 'U',
        (1, 0): 'U',
        (0, 0): 'R',
        (0, 1): 'R',
        (0, 2): 'R',
        (1, 2): 'U',
        (2, 1): 'L',
        (2, 2): 'U',
        (2, 3): 'L',
    }

    """ Realizamos el entrenamiento """
    n = 10000
    Deltas = []
    t = 1.0
    for i in range(n):

        aprendizaje = ALPHA / t
        cambioMayor = 0 # Para ver la mejora del robot

        estados_acciones_retornos = generarEjemplo(politica,grid)

        estados_vistos = set() # Método de First-Visit
        for s,a,G in estados_acciones_retornos:

            # Método de First-Visit
            if s not in estados_vistos:
                estados_vistos.add(s)
                theta_antiguo = theta.copy()
                x = convertirS_X(s)
                V_hat = theta.dot(x)
                theta += aprendizaje * (G - V_hat)*x
                cambioMayor = max(cambioMayor,np.abs(theta_antiguo - theta).sum())

        Deltas.append(cambioMayor) # Guardamos el mayor error de lla iteración actual


    plt.plot(Deltas)
    plt.show()

    V = {}
    estados = grid.todos_estados()
    for s in estados:
        if s in grid.acciones:
            V[s] = theta.dot(convertirS_X(s))
        else:
            # terminal state or state we can't otherwise get to
            V[s] = 0

    print("Valores Finales")
    mostrar_valores(V,grid)