from Abraham.Código._7_DP import Grid
from Abraham.Código._7_DP.iteracion_del_valor import mostrar_politica, mostrar_valores
import numpy as np
import matplotlib.pyplot as plt

GAMMA = 0.99

def jugar(politica,grid):

    """
        Elegimos un estado inicial random y una acción inical random
    """

    posiblesComienzos = list(grid.acciones.keys()) # Guardamos las claves de los iniciales
    inicial = np.random.choice(len(posiblesComienzos)) # Escogemos un comienzo aleatorio
    grid.set_estado(posiblesComienzos[inicial])

    a = np.random.choice(grid.posiblesAccionesBasicas())
    s = grid.estado_actual()
    estados_acciones_recompensas = [(s,a,0)] # El primero no tiene recompensas
    estados_visitados = set()
    estados_visitados.add(s)

    acabado = False
    while not acabado:

        """
            Hay que recordar que la recompensa en t=1 viene dada por haber elegido una acción
            en t=-1 estando en el estado de t=-1, es decir, en las tripletas la recompensa que
            insertamos es para la acción elegida en el estado anterior
        """

        r = grid.mover(a)
        s = grid.estado_actual()

        # Hemos pasado 2 veces por el mismo estado
        if s in estados_visitados:
            r = -10
            estados_acciones_recompensas.append((s,None,r))
            acabado = True

        # Hemos llegado a un estado terminal
        elif grid.game_over():
            estados_acciones_recompensas.append((s,None,r))
            acabado = True

        else:
            a = politica[s]
            estados_acciones_recompensas.append((s,a,r))

        estados_visitados.add(s)

    G = 0
    estados_acciones_retornos = []
    primero = True # La primera tripleta corresponderá al estado terminal, que no tiene ninguna futura recompensa

    for s,a,r in reversed(estados_acciones_recompensas):

        if primero:
            primero = False

        else:
            estados_acciones_retornos.append((s,a,G))

        G = r + GAMMA * G

    estados_acciones_retornos.reverse()
    return estados_acciones_retornos

"""
    Inicializamos los valores de 'Q', 'Politica' y
    'Estados_Acciones_Retornos'
"""
def iniciarValores(grid):

    todosEstados = grid.todos_estados()

    Q = {}  # Guardaremos Q(s,a) para todos los estados y acciones
    politica = {}  # Acciones a tomar en cada estado
    historialRetornos = {}  # Guardaremos todos los retornos para todos los estados y acciones

    for s in todosEstados:

        # Solo habrá cambios en los estados NO-TERMINALES
        if s in grid.acciones:
            politica[s] = np.random.choice(grid.posiblesAccionesBasicas())
            Q[s] = {}

            for a in grid.posiblesAccionesBasicas():
                Q[s][a] = 0
                historialRetornos[(s,a)] = []

    return (Q,politica,historialRetornos)


def MaxQ(Q_s):

    MaxV = float('-inf')
    MaxA = None

    for k,v in Q_s.items():
        if v > MaxV:
            MaxV = v
            MaxA = k

    return (MaxV,MaxA)


if __name__ == "__main__":

    grid = Grid.grid_negativo(penalizacion=-0.2)
    Q,politica,historialRetornos = iniciarValores(grid)

    print("Recompensas")
    mostrar_valores(grid.recompensas,grid)

    print("\nPolítica Inicial")
    mostrar_politica(politica,grid)

    print("\nValores Iniciales")
    V = {}
    for s in politica:
        V[s] = MaxQ(Q[s])[0]
    mostrar_valores(V, grid)


    episodios = 10000

    deltas = []

    for i in range(episodios):

        cambio_mayor = 0 # Nos servirá para comprobar la evolución del algoritmo
        estados_acciones_retornos = jugar(politica,grid)
        estados_acciones_vistos = set()

        # Actualizamos los valores de Q(s,a)
        for s,a,G in estados_acciones_retornos:

            sa = (s,a)

            if sa not in estados_acciones_vistos:
                Q_antiguo = Q[s][a] # Guardamos el valor antiguo
                historialRetornos[sa].append(G) # Guardamos el retorno en el historial
                Q[s][a] = np.mean(historialRetornos[sa]) # Actualizamos el valor de Q(s,a)
                cambio_mayor = max(cambio_mayor, abs(Q_antiguo - Q[s][a]))

                estados_acciones_vistos.add(sa)

        deltas.append(cambio_mayor)

        # Actualizamos la política
        for s in politica:
            politica[s] = MaxQ(Q[s])[1] # Nos quedamos con la mejor acción


    plt.plot(deltas)
    plt.show()


    print("\nPolítica Final")
    mostrar_politica(politica,grid)

    print("\nValores Finales")
    V = {}
    for s in politica:
        V[s] = MaxQ(Q[s])[0]
    mostrar_valores(V,grid)














