import numpy as np
import pandas as pd
import json

from Abraham._6_3Raya.Agente import Agente
from Abraham._6_3Raya.Ambiente import Ambiente
from Abraham._6_3Raya.Humano import Humano

"""
    Seteamos los valores iniciales V's para el
    jugador X
"""
def setearValoresV_x(env,tripletas):

    # Matriz vacía con el tamaño de la cantidad de estados posibles
    valoresV = np.zeros(env.cantEstados)

    # Recorremos cada uno de los posibles estados
    for estado, ganador, terminado in tripletas:
        if terminado:
            if ganador == env.x:
                v = 1 # Si ganó X, guardamos la victoria
            else:
                v = 0 # Perdió
        else:
            v = 0.5 # Quedamos empate

        valoresV[estado] = v
    return valoresV

"""
    Seteamos los valores iniciales V's para el
    jugador O
"""
def setearValoresV_o(env,tripletas):
    # Matriz vacía con el tamaño de la cantidad de estados posibles
    valoresV = np.zeros(env.cantEstados)

    # Recorremos cada uno de los posibles estados
    for estado, ganador, terminado in tripletas:
        if terminado:
            if ganador == env.o:
                v = 1  # Si ganó O, guardamos la victoria
            else:
                v = 0  # Perdió
        else:
            v = 0.5  # Quedamos empate

        valoresV[estado] = v
    return valoresV

"""
    Obtenemos cada posible estado del tablero (relleno por completo).
    * Si no tenemos ganador(None) ni hemos acabado el juego(False), significa que 
      hay empate.
    ** Recorremos el tablero de forma inversa, probando cada uno de los estados
       que pueda tomar.
"""
def obtener_hashEstados_y_ganador(env, i=0, j=0):
    results = []

    for v in (0, env.x, env.o):
        env.tablero[i, j] = v  # if empty board it should already be 0

        if j == 2:
            # j goes back to 0, increase i, unless i = 2, then we are done
            if i == 2:
                # the board is full, collect results and return
                estado = env.obtenerEstado()
                terminado = env.gameOver(forzar_recalculo=True)
                ganador = env.ganador
                results.append((estado, ganador, terminado))

            else:
                results += obtener_hashEstados_y_ganador(env, i + 1, 0)
        else:
            # increment j, i stays the same
            results += obtener_hashEstados_y_ganador(env, i, j + 1)

    return results

def jugar(p1, p2, env, dibujar=False):

    jugador_actual = None

    while not env.gameOver():
        if jugador_actual == p1:
            jugador_actual = p2
        else:
            jugador_actual = p1

        # Dibujamos el tablero antes de tomar una accion
        if dibujar:
            if dibujar == 1 and jugador_actual == p1:
                env.dibujarTablero()
            if dibujar == 2 and jugador_actual == p2:
                env.dibujarTablero()

        # El jugador toma una acción
        jugador_actual.tomarAccion(env)

        # Añadimos el estado actual a los historiales
        # de los jugadores
        estado = env.obtenerEstado()
        p1.añadir_estado_al_historial(estado)
        p2.añadir_estado_al_historial(estado)

    # Actualizamos las funciones de valor de
    # los jugadores V(s)
    p1.actualizacion(env)
    p2.actualizacion(env)



def guardarVsX(Vs):
    """
        Guarda los valores V's para el juegador "X"
    """
    data = pd.Series(Vs).to_json(orient='values')
    with open('ia.json', 'w', encoding='utf-8') as f:
        f.write(data)

def cargarVsX():
    """
        Carga los valores V's para el jugador "X"
    """
    with open('ia.json', encoding='utf-8') as f:
        data = json.load(f)
        print("Valores cargados con éxito")
    return data

def colores(color = ""):
    """
        Caambiamos el color de la consola
    """
    if color == "Verde":
        return '\033[92m'
    elif color == "Rojo":
        return '\033[91m'
    elif color == "Azul":
        return '\033[94m'
    else:
        return '\033[0m'


if __name__ == "__main__":

    env = Ambiente()

    p1 = Agente()
    p1.setSimbolo(env.x)
    p2 = Agente()
    p2.setSimbolo(env.o)

    estados_ganador_tripleta = obtener_hashEstados_y_ganador(env)

    Vx = setearValoresV_x(env, estados_ganador_tripleta)
    Vo = setearValoresV_o(env, estados_ganador_tripleta)

    # Guardamos los valores iniciales V(s) del jugador X
    p1.setValue(Vx)  # Les seteamos los valores correspondientes

    # Guardamos los valores iniciales V(s) del jugador O
    p2.setValue(Vo)  # Les seteamos los valores correspondientes

    """t = 10000
    for i in range(t):
        if i % 200 == 0:
            print(i)
        jugar(p1,p2,Ambiente())"""

    # Guarda los valores V's del jugador X
    #guardarVsX(p1.value)

    # Carga los valores V's del jugador X
    #p1.setValue(cargarVsX())


    # Para una partida normal
    humano = Humano(env.o)
    while True:
        env2 = Ambiente()
        jugar(p1, humano, env2, dibujar=2)

        ganador = colores("Verde") + "Ganastes!!" + colores() if env2.ganador == p2.simbolo else colores("Rojo") + "Has perdido :(" + colores() if env2.ganador == p1.simbolo else colores("Azul") + "Empate" + colores()
        print(ganador)
        env2.dibujarTablero()
        answer = input("Jugar otra vez? [S/N]: ")
        if answer and answer.lower()[0] == 'n':
            break