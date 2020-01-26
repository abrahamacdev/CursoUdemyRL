posiblesAccionesBasicas = ('U','R','D','L')

class Grid:

    def __init__(self, ancho, alto, comienzo):
        self.alto = alto
        self.ancho = ancho
        self.i = comienzo[0] # Fila de comienzo
        self.j = comienzo[1] # Columna de comienzo

    """
        Nos ayuda a setear las acciones y las recompensas del ambiente simultáneamente
    """
    def set(self, recompensas, acciones):
        # recompensas debe de ser un diccionario/map de: (i,j) -> recompensa  {(fila,columna):r}
        # accioes debe de ser una tupla de: (i,j) -> lista de posibles acciones {(fila,columna) -> acciones}
        self.recompensas = recompensas
        self.acciones = acciones

    """
        Indicamos al mundo donde estamos, para que nos pueda decir
        los siguientes estados
    """
    def set_estado(self, s):
        self.i = s[0]
        self.j = s[1]

    """
        Nos ayuda a saber cuál es nuestro estado actual
    """
    def estado_actual(self):
        return (self.i,self.j)

    """
        Nos ayuda a saber si el #estado es terminal
    """
    def es_terminal(self,estado):
        return estado not in self.acciones

    """
        Nos ayuda a movernos por el mundo
        #accion -> {'U','R','D','L'}
    """
    def mover(self,accion):
        # Comprobamos que el movimiento sea legal
        if accion in self.acciones[(self.i,self.j)]:
            if accion == 'U':
                self.i -= 1
            if accion == 'R':
                self.j += 1
            if accion == 'D':
                self.i += 1
            if accion == 'L':
                self.j -= 1

        # Retornamos la recompensa (si la hubiese)
        return self.recompensas.get((self.i,self.j),0)


    """
        Nos ayuda a deshacer un movimiento
        #accion -> {'U','R','D','L'}
    """
    def deshacer_movimiento(self,accion):
        if accion == 'U':
            self.i += 1
        if accion == 'R':
            self.j -= 1
        if accion == 'D':
            self.i += 1
        if accion == 'L':
            self.j -= 1

        # Lanzamos un error si llegamos a un estado en el que no
        # deberíamos de estar
        assert(self.estado_actual() in self.todos_estados())

    """
        Comprobamos si el juego terminó asegurandonos que en el estado
        actual no hay acciones posibles
    """
    def game_over(self):
        return (self.i,self.j) not in self.acciones

    """
        Obtenemos todos los estados posibles
    """
    def todos_estados(self):
        return set(self.acciones.keys() | self.recompensas.keys())



def grid_estandar():
    """
        Definimos un mundo que describe las recompensas obtenidas en cada estado
        y las acciones que podemos tomar en cada estado
        x -> No podemos pasar por ahí
        c -> Lugar de comienzo
        {-1,1} -> Recompensas del estado
        . . . 1
        . x . -1
        s . . .
    """
    comienzo = (2,0)
    g = Grid(3,4,comienzo)
    recompensas = {(0,3): 1, (1,3): -1}
    acciones = {
        (0,0): ('D','R'),
        (0,1): ('L','R'),
        (0, 2): ('D','R','L'),
        (1, 0): ('U','D'),
        (1, 2): ('U','R','D'),
        (2, 0): ('U','R'),
        (2, 1): ('L','R'),
        (2, 2): ('U','R','L'),
        (2, 3): ('U','L')
    }
    g.set(recompensas,acciones)
    return g

def grid_negativo(penalizacion=0.1):

    """
        Minimizamos el número de pasos tomados por el robot
        penalizando cada movimiento que puede tomar
    """

    g = grid_estandar()
    g.recompensas.update({
        (0, 0): penalizacion,
        (0, 1): penalizacion,
        (0, 2): penalizacion,
        (1, 0): penalizacion,
        (1, 2): penalizacion,
        (2, 0): penalizacion,
        (2, 1): penalizacion,
        (2, 2): penalizacion,
        (2, 3): penalizacion
    })
    return g

