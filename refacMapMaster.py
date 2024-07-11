import heapq

class Nodo:
    def __init__(self, x, y, g=float('inf'), h=0, f=float('inf'), parent=None):
        self.x = x
        self.y = y
        self.g = g  # Costo acumulado  
        self.h = h  # Heuristica
        self.f = f  # Costo total
        self.parent = parent  
    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Mapa:
    def __init__(self, n_filas, n_columnas):
        self.n_filas = n_filas
        self.n_columnas = n_columnas
        self.tablero = [[0 for _ in range(n_columnas)] for _ in range(n_filas)]

    def agregar_obstaculo(self):
        while True:
            print("Ingresa las coordenadas del obstáculo (x y), o 'fin' para terminar:")
            entrada = input()
            if entrada.lower() == 'fin':
                break
            try:
                x, y = map(int, entrada.split())
                if self.tablero[x][y] == 0:
                    self.tablero[x][y] = 1 
                else:
                    print("Ya hay un obstáculo en esa posición.")
            except (ValueError, IndexError):
                print("Coordenadas inválidas. Intenta nuevamente.")

    def obtener_coordenadas(self, mensaje):
        while True:
            try:
                entrada = input(mensaje)
                x, y = map(int, entrada.split())
                return (x, y)
            except ValueError:
                print("Por favor, ingresa dos números enteros separados por espacio.")

    def encontrar_ruta(self, inicio, objetivo):
        nodos_abiertos = []
        nodos_cerrados = []

        nodo_inicio = Nodo(inicio[0], inicio[1])
        nodo_objetivo = Nodo(objetivo[0], objetivo[1])

        heapq.heappush(nodos_abiertos, nodo_inicio)
        nodo_inicio.g = 0
        nodo_inicio.f = self.calcular_f(nodo_inicio, nodo_objetivo)

        while nodos_abiertos:
            nodo_actual = heapq.heappop(nodos_abiertos)
            if nodo_actual == nodo_objetivo:
                return self.construir_camino(nodo_actual)

            nodos_cerrados.append(nodo_actual)
            vecinos = self.obtener_vecinos(nodo_actual)
            for vecino in vecinos:
                if vecino in nodos_cerrados:
                    continue    
                nuevo_costo_g = nodo_actual.g + 1  # Costo uniforme, todos los movimientos tienen el mismo costo

                if nuevo_costo_g < vecino.g:
                    vecino.parent = nodo_actual
                    vecino.g = nuevo_costo_g
                    vecino.h = self.calcular_f(vecino, nodo_objetivo)
                    vecino.f = vecino.g + vecino.h
                    heapq.heappush(nodos_abiertos, vecino)

        return None  # No se encontró ruta válida

    def obtener_vecinos(self, nodo):
        vecinos = []
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Movimientos arriba, abajo, izquierda, derecha
        for dx, dy in direcciones:
            x_vecino, y_vecino = nodo.x + dx, nodo.y + dy
            if 0 <= x_vecino < self.n_filas and 0 <= y_vecino < self.n_columnas:
                if self.tablero[x_vecino][y_vecino] != 1:  # No es un obstáculo
                    vecino = Nodo(x_vecino, y_vecino)
                    vecinos.append(vecino)
        return vecinos


    def calcular_f(self, nodo, objetivo):
        return abs(nodo.x - objetivo.x) + abs(nodo.y - objetivo.y)


    def construir_camino(self, nodo_final):
        camino = []
        nodo_actual = nodo_final


        while nodo_actual is not None:
            camino.append((nodo_actual.x, nodo_actual.y))
            nodo_actual = nodo_actual.parent

        return camino[::-1]


    def imprimir_tablero_con_ruta(self, ruta, inicio, destino):
        tablero_con_ruta = [fila[:] for fila in self.tablero]
        tablero_con_ruta[inicio[0]][inicio[1]] = 'i'
        tablero_con_ruta[destino[0]][destino[1]] = 'd'

        for paso in ruta:
            x, y = paso
            if tablero_con_ruta[x][y] != 'i' and tablero_con_ruta[x][y] != 'd':
                tablero_con_ruta[x][y] = '.'
    
        for fila in tablero_con_ruta:
            for celda in fila:
                print(celda, end=' ')
            print()

if __name__ == "__main__":
    n_filas = 10
    n_columnas = 10

    mapa = Mapa(n_filas, n_columnas)

    mapa.agregar_obstaculo()

    inicio = mapa.obtener_coordenadas("Ingresa las coordenadas del punto de inicio (x y): ")
    destino = mapa.obtener_coordenadas("Ingresa las coordenadas del punto de destino (x y): ")

    ruta = mapa.encontrar_ruta(inicio, destino)

    if ruta:
        print("Ruta encontrada:")
        mapa.imprimir_tablero_con_ruta(ruta, inicio, destino)
    else:
        print("No se encontró ruta válida.")
