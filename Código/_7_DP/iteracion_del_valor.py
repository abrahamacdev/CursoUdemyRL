import numpy as np
import time
from Abraham.Código._7_DP import Grid

LIMITE = 10e-3 # Límite para la convergencia

"""
    Mostramos los valores V(s) de la politica
"""
def mostrar_valores(V,g):
    for i in range(g.ancho):
        print("------------------------")
        for j in range(g.alto):
            v = V.get((i,j),0)
            if v >= 0:
                print(" %.2f|" % v, end="")
            else:
                print("%.2f|" % v, end="") # -ve tiene un espacio extra
        print("")
    print("------------------------")


"""
    Mostramos los movimientos de nuestra política 
"""
def mostrar_politica(P,g):
    for i in range(g.ancho):
        print("----------------")
        for j in range(g.alto):
            a = P.get((i,j),' ')
            print(" %s |" % a, end="")
        print("")
    print("----------------")

if __name__ == "__main__":


    """
        Dada una política, encontramos los valores V(s).
        Vamos a hacer esto tanto para una "política aletoria random" como
        para una "política fija (determinista)"
        NOTA:
        ♦ La aleatoriedad proviene de dos lugares
        ♦ p(a|s) -> Decide que acción tomar dado un estado
        ♦ p(s',r|s,a) -> El estado al que llegaremos y la recompensa que obtendremos dado un estado y una acción
        ♦ De momento p(a|s) tendra  una distribución uniforme (todos la misma probabilidad)
        ☺ ¿Cómo cambiaría el código si p(s',r|s,a) no fuese determinista?
    """
    grid = Grid.grid_estandar()


    # Los estados serán posiciones (i,j)
    estados = grid.todos_estados()

    GAMMA = 0.9 # Factor de descuento

    politica = {}
    for s in estados:
        if s in grid.acciones:
            politica[s] = np.random.choice(grid.posiblesAccionesBasicas())

    print("Política antes de mejora")
    mostrar_politica(politica,grid)
    print("\n\n")

    # Inicializamos todos los estados a cero
    V = {}
    for s in estados:
        V[s] = 0

    """ Forma 1 """
    while True:
        cambio_mayor = 0  # Delta
        for s in estados:
            v_antigua = V[s]

            # V(s) solo tendrá valor si no es un estado terminal
            if s in politica:

                maxV = float('-inf')
                for a in grid.posiblesAccionesBasicas():
                    grid.set_estado(s) # Nos posicionamos en un nuevo estado para probar
                    r = grid.mover(a) # Recompensa de llegar al nuevo estado (s')
                    v = r + GAMMA * V[grid.estado_actual()]

                    # Nos quedamos con el valor del estado tomando
                    # la mejor acción
                    if v > maxV:
                        maxV = v # Guardamos el máximo valor de V

                V[s] = maxV  # Guardamos el valor en el map

            cambio_mayor = max(cambio_mayor, np.abs(v_antigua - V[s]))

        if cambio_mayor < LIMITE:
            break

    # Escogemos las acciones de nuestra política
    # con ayuda de los valores V(s)
    for s in politica.keys():
        max_v = float('-inf')
        max_a = None

        for a in grid.posiblesAccionesBasicas():
            grid.set_estado(s)  # Nos posicionamos en un nuevo estado para probar
            r = grid.mover(a)  # Recompensa de llegar al nuevo estado (s')
            v = r + GAMMA * V[grid.estado_actual()]

            if v > max_v:
                max_v = v
                max_a = a

        politica[s] = max_a

    print("Política final")
    mostrar_politica(politica,grid)



    """ Forma 2 """
    """
    # Iteracion del Valor
    while True:
        cambio_mayor = 0  # Delta
        for s in estados:
            v_antigua = V[s]

            # V(s) solo tendrá valor si no es un estado terminal
            if s in politica:

                maxV = float('-inf')
                max_A = None

                for a in grid.posiblesAccionesBasicas():
                    grid.set_estado(s) # Nos posicionamos en un nuevo estado para probar
                    r = grid.mover(a) # Recompensa de llegar al nuevo estado (s')
                    v = r + GAMMA * V[grid.estado_actual()]

                    # Nos quedamos con el valor del estado tomando
                    # la mejor acción
                    if v > maxV:
                        maxV = v # Guardamos el máximo valor de V
                        max_A = a

                V[s] = maxV  # Guardamos el valor en el map
                politica[s] = max_A

            cambio_mayor = max(cambio_mayor, np.abs(v_antigua - V[s]))

        if cambio_mayor < LIMITE:
            break

    print("Política final 2")
    mostrar_politica(politica, grid)
    """