import numpy as np
import random

class CrossSudokuGA:
    def __init__(self, tam_poblacion=500, prob_mutacion=0.15):
        self.tam_poblacion = tam_poblacion
        self.prob_mutacion = prob_mutacion
        
        # Estructura del Cross Sudoku (5 grids de 9x9)
        self.grids = {
            'center': None,    # Grid central (compartido)
            'top': None,       # Grid superior
            'bottom': None,    # Grid inferior
            'left': None,      # Grid izquierdo
            'right': None      # Grid derecho
        }
        
        # Inicializar con el puzzle de la imagen
        self.inicializar_puzzle_desde_imagen()

        def inicializar_puzzle_desde_imagen(self):
    """Inicializa el puzzle basado en la imagen proporcionada"""
    
    # Grid central (completamente lleno en la imagen)
    self.grids['center'] = np.array([
        [8, 5, 9, 3, 8, 6, 5, 3, 4],
        [9, 1, 2, 8, 5, 3, 7, 5, 9],
        [3, 7, 6, 4, 9, 1, 8, 5, 2],
        [6, 2, 8, 1, 5, 4, 7, 6, 3],
        [1, 9, 8, 4, 7, 3, 2, 4, 9],
        [5, 3, 4, 6, 2, 7, 8, 1, 6],
        [4, 1, 2, 9, 6, 5, 7, 3, 2],
        [6, 5, 3, 1, 9, 4, 8, 6, 1],
        [8, 9, 5, 4, 1, 7, 3, 2, 4]
    ])
    
    # Grid superior (parcialmente lleno)
    self.grids['top'] = np.array([
        [3, 8, 5, 6, 4, 2, 7, 0, 0],
        [9, 6, 8, 2, 7, 5, 3, 0, 0],
        [2, 7, 4, 9, 5, 3, 6, 0, 0],
        [5, 9, 2, 3, 8, 1, 4, 0, 0],
        [2, 9, 6, 5, 5, 3, 0, 0, 0],
        [7, 8, 6, 1, 9, 3, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    
    # Grid inferior (parcialmente lleno)
    self.grids['bottom'] = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [3, 5, 2, 4, 9, 7, 8, 0, 0],
        [7, 2, 1, 9, 3, 0, 0, 0, 0],
        [3, 4, 9, 9, 0, 0, 0, 0, 0],
        [6, 2, 8, 1, 7, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    
    # Grid izquierdo (parcialmente lleno)
    self.grids['left'] = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    
    # Grid derecho (parcialmente lleno)
    self.grids['right'] = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    
    # Identificar celdas fijas (diferentes de 0)
    self.celdas_fijas = {}
    for grid_name, grid in self.grids.items():
        self.celdas_fijas[grid_name] = (grid != 0)


def calcular_fitness(self, individuo):
    """Calcula el fitness considerando todas las restricciones del Cross Sudoku"""
    fitness_total = 0
    
    # Verificar restricciones en cada grid individual
    for grid_name in ['center', 'top', 'bottom', 'left', 'right']:
        grid = individuo[grid_name]
        fitness_total += self._fitness_grid(grid, grid_name)
    
    # Verificar restricciones entre grids conectados
    fitness_total += self._fitness_conexiones(individuo)
    
    return fitness_total

def _fitness_grid(self, grid, grid_name):
    """Calcula fitness para un grid individual"""
    fitness = 0
    
    # Verificar filas
    for i in range(9):
        fila = grid[i, :]
        fitness += (9 - len(set(fila))) * 10  # Penalizar duplicados
    
    # Verificar columnas
    for j in range(9):
        columna = grid[:, j]
        fitness += (9 - len(set(columna))) * 10  # Penalizar duplicados
    
    # Verificar subcuadros 3x3
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            subcuadro = grid[i:i+3, j:j+3].flatten()
            fitness += (9 - len(set(subcuadro))) * 5  # Penalizar duplicados
    
    # Penalizar cambios en celdas fijas
    cambios = np.sum((grid != self.grids[grid_name]) & self.celdas_fijas[grid_name])
    fitness += cambios * 100  # Alta penalización por cambiar celdas fijas
    
    return -fitness  # Convertir a negativo (mayor es mejor)

def _fitness_conexiones(self, individuo):
    """Verifica restricciones entre grids conectados"""
    fitness = 0
    
    # Conexión entre grid central y superior
    for j in range(9):
        if individuo['center'][0, j] != individuo['top'][8, j]:
            fitness -= 5  # Penalizar inconsistencias
    
    # Conexión entre grid central e inferior
    for j in range(9):
        if individuo['center'][8, j] != individuo['bottom'][0, j]:
            fitness -= 5
    
    # Conexión entre grid central e izquierdo
    for i in range(9):
        if individuo['center'][i, 0] != individuo['left'][i, 8]:
            fitness -= 5
    
    # Conexión entre grid central y derecho
    for i in range(9):
        if individuo['center'][i, 8] != individuo['right'][i, 0]:
            fitness -= 5
    
    return fitness
def inicializar_poblacion(self):
    """Inicializa la población respetando las celdas fijas"""
    poblacion = []
    
    for _ in range(self.tam_poblacion):
        individuo = {}
        
        # Inicializar cada grid
        for grid_name in self.grids.keys():
            grid_original = self.grids[grid_name]
            nuevo_grid = grid_original.copy()
            
            # Llenar celdas vacías manteniendo restricciones de subcuadrícula
            if grid_name != 'center':  # El centro ya está completo
                for i in range(0, 9, 3):
                    for j in range(0, 9, 3):
                        subcuadro = nuevo_grid[i:i+3, j:j+3]
                        numeros_faltantes = self._obtener_numeros_faltantes(subcuadro)
                        random.shuffle(numeros_faltantes)
                        
                        # Llenar celdas vacías
                        idx = 0
                        for x in range(3):
                            for y in range(3):
                                if nuevo_grid[i+x, j+y] == 0:
                                    nuevo_grid[i+x, j+y] = numeros_faltantes[idx]
                                    idx += 1
            
            individuo[grid_name] = nuevo_grid
        
        poblacion.append(individuo)
    
    return poblacion

def _obtener_numeros_faltantes(self, subcuadro):
    """Devuelve números del 1-9 que faltan en el subcuadro"""
    todos_numeros = set(range(1, 10))
    presentes = set(subcuadro.flatten()) - {0}
    return list(todos_numeros - presentes)

def seleccionar_padres(self, poblacion, fitness):
    """Selección por torneo para Cross Sudoku"""
    padres = []
    
    for _ in range(2):  # Seleccionar 2 padres
        # Torneo de tamaño 3
        candidatos = random.sample(list(zip(poblacion, fitness)), 3)
        # Elegir el mejor del torneo
        mejor = max(candidatos, key=lambda x: x[1])
        padres.append(mejor[0])
    
    return padres

def cruzar(self, padre1, padre2):
    """Cruce especializado para Cross Sudoku"""
    hijo = {}
    
    # Para cada grid, decidir de qué padre heredar
    for grid_name in self.grids.keys():
        if random.random() < 0.5:
            hijo[grid_name] = padre1[grid_name].copy()
        else:
            hijo[grid_name] = padre2[grid_name].copy()
    
    # Asegurar que se mantengan las celdas fijas
    for grid_name in self.grids.keys():
        hijo[grid_name][self.celdas_fijas[grid_name]] = self.grids[grid_name][self.celdas_fijas[grid_name]]
    
    return hijo
def mutar(self, individuo):
    """Mutación especializada para Cross Sudoku"""
    for grid_name in self.grids.keys():
        if grid_name != 'center' and random.random() < self.prob_mutacion:
            grid = individuo[grid_name]
            
            # Elegir un subcuadro aleatorio para mutar
            i_sub = random.randint(0, 2) * 3
            j_sub = random.randint(0, 2) * 3
            
            # Encontrar celdas no fijas en el subcuadro
            celdas_mutables = []
            for i in range(3):
                for j in range(3):
                    if not self.celdas_fijas[grid_name][i_sub+i, j_sub+j]:
                        celdas_mutables.append((i_sub+i, j_sub+j))
            
            if len(celdas_mutables) >= 2:
                # Elegir dos celdas aleatorias e intercambiar valores
                celda1, celda2 = random.sample(celdas_mutables, 2)
                grid[celda1], grid[celda2] = grid[celda2], grid[celda1]
    
    return individuo
def ejecutar(self, generaciones=1000):
    """Ejecuta el algoritmo genético para Cross Sudoku"""
    poblacion = self.inicializar_poblacion()
    mejor_fitness = float('-inf')
    mejor_individuo = None
    historial_fitness = []
    
    for generacion in range(generaciones):
        # Calcular fitness
        fitness_poblacion = [self.calcular_fitness(ind) for ind in poblacion]
        
        # Encontrar el mejor
        max_fitness = max(fitness_poblacion)
        if max_fitness > mejor_fitness:
            mejor_fitness = max_fitness
            mejor_individuo = self.copiar_individuo(poblacion[fitness_poblacion.index(max_fitness)])
        
        historial_fitness.append(mejor_fitness)
        
        # Condición de término (solución perfecta)
        if mejor_fitness == 0:
            print(f"¡Solución encontrada en generación {generacion}!")
            break
        
        # Crear nueva población
        nueva_poblacion = []
        
        # Elitismo: mantener el mejor individuo
        nueva_poblacion.append(self.copiar_individuo(mejor_individuo))
        
        while len(nueva_poblacion) < self.tam_poblacion:
            # Selección
            padre1, padre2 = self.seleccionar_padres(poblacion, fitness_poblacion)
            
            # Cruce
            hijo = self.cruzar(padre1, padre2)
            
            # Mutación
            hijo = self.mutar(hijo)
            
            nueva_poblacion.append(hijo)
        
        poblacion = nueva_poblacion
        
        # Mostrar progreso
        if generacion % 50 == 0:
            print(f"Gen {generacion}: Mejor fitness = {mejor_fitness}")
    
    return mejor_individuo, mejor_fitness, historial_fitness

def copiar_individuo(self, individuo):
    """Crea una copia profunda de un individuo"""
    copia = {}
    for grid_name, grid in individuo.items():
        copia[grid_name] = grid.copy()
    return copia
def visualizar_cross_sudoku(self, individuo):
    """Visualiza el Cross Sudoku completo"""
    print("Cross Sudoku - Solución:")
    print("=" * 50)
    
    # Visualizar grid superior
    print("Grid Superior:")
    self.visualizar_grid(individuo['top'])
    print()
    
    # Visualizar grids izquierdo, central y derecho en una fila
    print("Grids Izquierdo, Central y Derecho:")
    for i in range(9):
        fila_izq = " ".join(str(x) if x != 0 else "." for x in individuo['left'][i, :])
        fila_cen = " ".join(str(x) if x != 0 else "." for x in individuo['center'][i, :])
        fila_der = " ".join(str(x) if x != 0 else "." for x in individuo['right'][i, :])
        print(f"{fila_izq} | {fila_cen} | {fila_der}")
    print()
    
    # Visualizar grid inferior
    print("Grid Inferior:")
    self.visualizar_grid(individuo['bottom'])
    print("=" * 50)

def visualizar_grid(self, grid):
    """Visualiza un grid individual de forma legible"""
    print("+" + "---+" * 9)
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("+" + "---+" * 9)
        
        fila = "|"
        for j in range(9):
            if j % 3 == 0 and j != 0:
                fila += " |"
            valor = grid[i, j]
            fila += f" {valor if valor != 0 else '.'} "
        fila += " |"
        print(fila)
    print("+" + "---+" * 9)
    # Crear y ejecutar el algoritmo
cross_sudoku_solver = CrossSudokuGA(tam_poblacion=300, prob_mutacion=0.2)
solucion, fitness, historial = cross_sudoku_solver.ejecutar(generaciones=2000)

# Mostrar resultados
print(f"Mejor fitness alcanzado: {fitness}")
cross_sudoku_solver.visualizar_cross_sudoku(solucion)

# Verificar si es solución completa
if fitness == 0:
    print("✅ ¡Solución válida encontrada!")
else:
    print("⚠️  Solución parcial encontrada. Intente con más generaciones.")