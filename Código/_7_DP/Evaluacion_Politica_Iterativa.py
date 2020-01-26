import numpy as np
from Abraham.Código._7_DP import Grid

LIMITE = 10e-5 # Límite para la convergencia

"""
    Mostramos los valores V(s) de la politica
"""
def mostrar_valores(V,g):
    for i in range(g.ancho):
        print("--------------------")
        for j in range(g.alto):
            v = V.get((i,j),0)
            if v >= 0:
                print(" %.2f|" % v, end="")
            else:
                print("%.2f|" % v, end="") # -ve tiene un espacio extra
        print("")


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

    """ Acciones Randoms con distribuciones uniformes """
    # Iniciamos V(s) = 0
    V = {}
    for s in estados:
        V[s] = 0

    gamma = 0.99 # Factor de descuento

    # Repetir hasta converger
    while True:
        cambio_mayor = 0 # Delta
        for s in estados:
            v_antigua = V[s]

            # V(s) solo tendrá valor si no es un estado terminal
            if s in grid.acciones:
                v_nueva = 0 # Acumulamos la respuesta
                p_a = 1.0 / len(grid.acciones[s]) #  Cada acción tendrá la misma probabilidad

                for a in grid.acciones[s]:
                    grid.set_estado(s) # s'
                    r = grid.mover(a)
                    v_nueva += p_a * (r + gamma * V[grid.estado_actual()])

                V[s] = v_nueva
                cambio_mayor = max(cambio_mayor, abs(v_antigua - V[s]))

        if cambio_mayor < LIMITE:
            break

    print("Valores para las acciones randoms con distribuciones uniformes")
    mostrar_valores(V,grid)
    print("\n\n")


    """ Acciones usando una política fija (determinista) """
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

    # Inicializamos todos los estados a cero
    V = {}
    for s in estados:
        V[s] = 0

    # Comprobemos como V(s) cambia conforme más nos alejamos de la recompensa
    gamma = 0.9  # Factor de descuento

    # Repetir hasta converger
    while True:
        cambio_mayor = 0  # Delta
        for s in estados:
            v_antigua = V[s]

            # V(s) solo tendrá valor si no es un estado terminal
            if s in politica:
                a = politica[s] # Obtenemos la acción de la política fija
                grid.set_estado(s) # Nos posicionamos en un nuevo estado para probar
                r = grid.mover(a) # Recompensa de llegar al nuevo estado (s')
                V[s] = r + gamma * V[grid.estado_actual()]
                cambio_mayor = max(cambio_mayor, np.abs(v_antigua - V[s]))

        if cambio_mayor < LIMITE:
            break

    print("Valores para la política determinista")
    mostrar_valores(V, grid)
    print("\n")

    print("Política determinista")
    mostrar_politica(politica,grid)
    print("\n\n")