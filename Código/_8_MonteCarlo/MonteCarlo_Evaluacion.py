from Abraham.Código._7_DP import Grid
import numpy as np

GAMMA = 0.9

def unaRonda(politica,grid = Grid.grid_estandar()):

    # Comenzamos en posiciones random para comprobar su
    # valor
    posiblesEstadosIniciales = list(grid.acciones.keys())
    inicial = np.random.choice(len(posiblesEstadosIniciales))
    grid.set_estado(posiblesEstadosIniciales[inicial])

    s = grid.estado_actual()
    print(s)
    s_r = [(s,0)]
    while not grid.game_over():
        a = politica[s]
        r = grid.mover(a)
        s = grid.estado_actual()
        s_r.append((s,r))

    G = 0
    s_retornos = []
    primeraVez = False
    for s,r in reversed(s_r):

        """ 
            El primer elemento se corresponde con el último estado, 
            que por definición siempre será 0
        """
        if not primeraVez:
            primeraVez = True

        else:
            s_retornos.append((s,G))
            G = r + GAMMA * G
    return reversed(s_retornos)




if __name__ == "__main__":

    grid = Grid.grid_estandar()
    todosEstados = grid.todos_estados()

    V = {}
    retornos = {}
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

    for s in todosEstados:
        if s in grid.acciones:
            retornos[s] = [] # Iremos acumulando los retornos de cada estado para aplicarles la media
        else:
            V[s] = 0 # Los estados terminales siempre = 0

    n = 5000

    for i in range(n):
        print("Llamada nº" + str(i))
        s_g = unaRonda(politica,grid)
        estados_vistos = set()

        for s,G in s_g:

            if not s in estados_vistos:
                retornos[s].append(G)
                V[s] = np.mean(retornos[s])
                estados_vistos.add(s)