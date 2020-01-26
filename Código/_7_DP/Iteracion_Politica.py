import numpy as np
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
    for s in grid.todos_estados():
        if s in grid.acciones:
            politica[s] = np.random.choice(grid.posiblesAccionesBasicas())

    print("Política antes de mejora")
    mostrar_politica(politica,grid)
    print("\n\n")

    # Inicializamos todos los estados a cero
    V = {}
    for s in estados:
        V[s] = 0

    while True:

        # Evaluación de la Política
        while True:
            cambio_mayor = 0  # Delta
            for s in estados:
                v_antigua = V[s]

                # V(s) solo tendrá valor si no es un estado terminal
                if s in politica:
                    a = politica[s] # Obtenemos la acción de la política fija
                    grid.set_estado(s) # Nos posicionamos en un nuevo estado para probar
                    r = grid.mover(a) # Recompensa de llegar al nuevo estado (s')
                    V[s] = r + GAMMA * V[grid.estado_actual()]
                    cambio_mayor = max(cambio_mayor, np.abs(v_antigua - V[s]))

            if cambio_mayor < LIMITE:
                break

        mostrar_valores(V,grid)
        print("*********************")
        mostrar_politica(politica,grid)
        print("\n\n")

        # Mejora de la política
        estable = True
        for s in estados:
            if s in politica:
                a_antigua = politica[s]  # Guardamos la antigua acción
                nueva_a = None           # Será la nueva acción que tomaremos
                mejor_v = float('-inf')  # Mejor V(s) hasta ahora

                for accion in grid.posiblesAccionesBasicas():
                    grid.set_estado(s) # Seteamos nuestro estado
                    r = grid.mover(accion) # Obtenemos la recompensa del estado
                    v = r + GAMMA * V[grid.estado_actual()]
                    # Comprobamos si el nuevo valor es mejor
                    if v > mejor_v:
                        mejor_v = v
                        nueva_a = accion
                        politica[s] = nueva_a # Guardamos la acción como la mejor que podemos tomar

                if a_antigua != nueva_a:
                    estable = False

        if estable:
            break;

    print("Valores de la política final")
    mostrar_valores(V, grid)
    print("\n")

    print("Política final")
    mostrar_politica(politica,grid)