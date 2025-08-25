import random
import time

class CrossSudokuGA:
    def __init__(self, tam_poblacion=200, prob_mutacion=0.25):
        self.tam_poblacion = tam_poblacion
        self.prob_mutacion = prob_mutacion
        
        # Estructura del Cross Sudoku (5 grids de 9x9)
        self.grids = {
            'center': None,
            'top': None,
            'bottom': None,
            'left': None,
            'right': None
        }
        
        # Inicializar el puzzle automáticamente
        self.inicializar_puzzle_automatico()
        
    def crear_grid_vacio(self):
        """Crea un grid 9x9 vacío"""
        return [[0 for _ in range(9)] for _ in range(9)]
    
    def copiar_grid(self, grid):
        """Copia un grid"""
        return [fila[:] for fila in grid]
    
    def es_valido_en_fila(self, grid, fila, num):
        """Verifica si un número es válido en la fila"""
        return num not in grid[fila]
    
    def es_valido_en_columna(self, grid, columna, num):
        """Verifica si un número es válido en la columna"""
        for i in range(9):
            if grid[i][columna] == num:
                return False
        return True
    
    def es_valido_en_subcuadro(self, grid, fila_inicio, columna_inicio, num):
        """Verifica si un número es válido en el subcuadro 3x3"""
        for i in range(3):
            for j in range(3):
                if grid[fila_inicio + i][columna_inicio + j] == num:
                    return False
        return True
    
    def es_valido(self, grid, fila, columna, num):
        """Verifica si un número es válido en la posición"""
        return (self.es_valido_en_fila(grid, fila, num) and
                self.es_valido_en_columna(grid, columna, num) and
                self.es_valido_en_subcuadro(grid, fila - fila % 3, columna - columna % 3, num))
    
    def resolver_sudoku(self, grid):
        """Resuelve un sudoku usando backtracking (para inicialización)"""
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    for num in random.sample(range(1, 10), 9):  # Números en orden aleatorio
                        if self.es_valido(grid, i, j, num):
                            grid[i][j] = num
                            if self.resolver_sudoku(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True
    
    def generar_sudoku_completo(self):
        """Genera un sudoku completo válido"""
        grid = self.crear_grid_vacio()
        self.resolver_sudoku(grid)
        return grid
    
    def remover_celdas(self, grid, celdas_a_remover=30):
        """Remueve celdas para crear un puzzle"""
        grid_copy = self.copiar_grid(grid)
        celdas_removidas = 0
        while celdas_removidas < celdas_a_remover:
            i, j = random.randint(0, 8), random.randint(0, 8)
            if grid_copy[i][j] != 0:
                grid_copy[i][j] = 0
                celdas_removidas += 1
        return grid_copy
    
    def inicializar_puzzle_automatico(self):
        """Inicializa automáticamente un Cross Sudoku válido"""
        print("🧩 Generando Cross Sudoku automáticamente...")
        
        # 1. Generar grid central completo
        self.grids['center'] = self.generar_sudoku_completo()
        print("✅ Grid central generado")
        
        # 2. Generar grids periféricos completos que sean compatibles
        self.grids['top'] = self.generar_grid_compatible(self.grids['center'], 'top')
        self.grids['bottom'] = self.generar_grid_compatible(self.grids['center'], 'bottom')
        self.grids['left'] = self.generar_grid_compatible(self.grids['center'], 'left')
        self.grids['right'] = self.generar_grid_compatible(self.grids['center'], 'right')
        
        print("✅ Grids periféricos generados")
        
        # 3. Remover celdas para crear el puzzle
        self.grids['top'] = self.remover_celdas(self.grids['top'], 40)
        self.grids['bottom'] = self.remover_celdas(self.grids['bottom'], 40)
        self.grids['left'] = self.remover_celdas(self.grids['left'], 40)
        self.grids['right'] = self.remover_celdas(self.grids['right'], 40)
        
        print("✅ Celdas removidas para crear el puzzle")
        
        # 4. Identificar celdas fijas
        self.celdas_fijas = {}
        for grid_name, grid in self.grids.items():
            self.celdas_fijas[grid_name] = self.crear_mascara_fijas(grid)
        
        print("✅ Cross Sudoku generado exitosamente!")
        self.mostrar_estado_inicial()
    
    def generar_grid_compatible(self, grid_central, posicion):
        """Genera un grid compatible con el grid central"""
        grid = self.crear_grid_vacio()
        
        # Llenar la fila/columna que se conecta con el grid central
        if posicion == 'top':
            # La última fila del top debe coincidir con la primera fila del centro
            grid[8] = grid_central[0][:]
        elif posicion == 'bottom':
            # La primera fila del bottom debe coincidir con la última fila del centro
            grid[0] = grid_central[8][:]
        elif posicion == 'left':
            # La última columna del left debe coincidir con la primera columna del centro
            for i in range(9):
                grid[i][8] = grid_central[i][0]
        elif posicion == 'right':
            # La primera columna del right debe coincidir con la última columna del centro
            for i in range(9):
                grid[i][0] = grid_central[i][8]
        
        # Resolver el resto del grid manteniendo las conexiones fijas
        self.resolver_sudoku_con_restricciones(grid, grid_central, posicion)
        return grid
    
    def resolver_sudoku_con_restricciones(self, grid, grid_central, posicion):
        """Resuelve un sudoku con restricciones de conexión"""
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    for num in random.sample(range(1, 10), 9):
                        if self.es_valido_con_restricciones(grid, i, j, num, grid_central, posicion):
                            grid[i][j] = num
                            if self.resolver_sudoku_con_restricciones(grid, grid_central, posicion):
                                return True
                            grid[i][j] = 0
                    return False
        return True
    
    def es_valido_con_restricciones(self, grid, fila, columna, num, grid_central, posicion):
        """Verifica validez con restricciones adicionales"""
        if not self.es_valido(grid, fila, columna, num):
            return False
        
        # Verificar restricciones de conexión
        if posicion == 'top' and fila == 8:
            # La última fila del top debe coincidir con la primera del centro
            return num == grid_central[0][columna]
        elif posicion == 'bottom' and fila == 0:
            # La primera fila del bottom debe coincidir con la última del centro
            return num == grid_central[8][columna]
        elif posicion == 'left' and columna == 8:
            # La última columna del left debe coincidir con la primera del centro
            return num == grid_central[fila][0]
        elif posicion == 'right' and columna == 0:
            # La primera columna del right debe coincidir con la última del centro
            return num == grid_central[fila][8]
        
        return True
    
    def crear_mascara_fijas(self, grid):
        """Crea máscara de celdas fijas"""
        return [[1 if cell != 0 else 0 for cell in row] for row in grid]
    
    def mostrar_estado_inicial(self):
        """Muestra el estado inicial del puzzle"""
        print("\n📊 Estado inicial del Cross Sudoku:")
        print("=" * 50)
        print(f"Grid Central: {self.contar_celdas_llenas(self.grids['center'])}/81 celdas llenas")
        print(f"Grid Superior: {self.contar_celdas_llenas(self.grids['top'])}/81 celdas llenas")
        print(f"Grid Inferior: {self.contar_celdas_llenas(self.grids['bottom'])}/81 celdas llenas")
        print(f"Grid Izquierdo: {self.contar_celdas_llenas(self.grids['left'])}/81 celdas llenas")
        print(f"Grid Derecho: {self.contar_celdas_llenas(self.grids['right'])}/81 celdas llenas")
        print("=" * 50)
    
    def contar_celdas_llenas(self, grid):
        """Cuenta celdas no vacías"""
        return sum(1 for fila in grid for cell in fila if cell != 0)
    
    # ... (el resto de los métodos se mantienen igual hasta calcular_fitness)
    
    def calcular_fitness(self, individuo):
        """Calcula el fitness considerando todas las restricciones"""
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
            fila = grid[i]
            fitness += (9 - len(set(fila))) * 10
        
        # Verificar columnas
        for j in range(9):
            columna = [grid[i][j] for i in range(9)]
            fitness += (9 - len(set(columna))) * 10
        
        # Verificar subcuadros 3x3
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                subcuadro = []
                for x in range(3):
                    for y in range(3):
                        subcuadro.append(grid[i + x][j + y])
                fitness += (9 - len(set(subcuadro))) * 5
        
        # Penalizar cambios en celdas fijas
        cambios = 0
        for i in range(9):
            for j in range(9):
                if self.celdas_fijas[grid_name][i][j] and grid[i][j] != self.grids[grid_name][i][j]:
                    cambios += 1
        fitness += cambios * 100
        
        return -fitness
    
    def _fitness_conexiones(self, individuo):
        """Verifica restricciones entre grids conectados"""
        fitness = 0
        
        # Conexión entre grid central y superior
        for j in range(9):
            if individuo['center'][0][j] != individuo['top'][8][j]:
                fitness -= 5
        
        # Conexión entre grid central e inferior
        for j in range(9):
            if individuo['center'][8][j] != individuo['bottom'][0][j]:
                fitness -= 5
        
        # Conexión entre grid central e izquierdo
        for i in range(9):
            if individuo['center'][i][0] != individuo['left'][i][8]:
                fitness -= 5
        
        # Conexión entre grid central y derecho
        for i in range(9):
            if individuo['center'][i][8] != individuo['right'][i][0]:
                fitness -= 5
        
        return fitness
    
    def inicializar_poblacion(self):
        """Inicializa la población respetando las celdas fijas"""
        poblacion = []
        
        for _ in range(self.tam_poblacion):
            individuo = {}
            
            for grid_name in self.grids.keys():
                grid_original = self.grids[grid_name]
                nuevo_grid = self.copiar_grid(grid_original)
                
                if grid_name != 'center':  # El centro ya está completo
                    # Llenar celdas vacías manteniendo restricciones
                    for i in range(0, 9, 3):
                        for j in range(0, 9, 3):
                            subcuadro = self.obtener_subcuadro(nuevo_grid, i, j)
                            numeros_faltantes = self._obtener_numeros_faltantes(subcuadro)
                            random.shuffle(numeros_faltantes)
                            
                            idx = 0
                            for x in range(3):
                                for y in range(3):
                                    if nuevo_grid[i + x][j + y] == 0:
                                        nuevo_grid[i + x][j + y] = numeros_faltantes[idx]
                                        idx += 1
                
                individuo[grid_name] = nuevo_grid
            
            poblacion.append(individuo)
        
        return poblacion
    
    def obtener_subcuadro(self, grid, i, j):
        """Obtiene subcuadro 3x3"""
        subcuadro = []
        for x in range(3):
            fila = []
            for y in range(3):
                fila.append(grid[i + x][j + y])
            subcuadro.append(fila)
        return subcuadro
    
    def _obtener_numeros_faltantes(self, subcuadro):
        """Devuelve números del 1-9 que faltan en el subcuadro"""
        todos_numeros = set(range(1, 10))
        presentes = set()
        for fila in subcuadro:
            for cell in fila:
                if cell != 0:
                    presentes.add(cell)
        return list(todos_numeros - presentes)
    
    def seleccionar_padres(self, poblacion, fitness):
        """Selección por torneo"""
        padres = []
        
        for _ in range(2):
            candidatos = random.sample(list(zip(poblacion, fitness)), 3)
            mejor = max(candidatos, key=lambda x: x[1])
            padres.append(mejor[0])
        
        return padres
    
    def cruzar(self, padre1, padre2):
        """Cruce especializado"""
        hijo = {}
        
        for grid_name in self.grids.keys():
            if random.random() < 0.5:
                hijo[grid_name] = self.copiar_grid(padre1[grid_name])
            else:
                hijo[grid_name] = self.copiar_grid(padre2[grid_name])
        
        # Mantener celdas fijas
        for grid_name in self.grids.keys():
            for i in range(9):
                for j in range(9):
                    if self.celdas_fijas[grid_name][i][j]:
                        hijo[grid_name][i][j] = self.grids[grid_name][i][j]
        
        return hijo
    
    def mutar(self, individuo):
        """Mutación especializada"""
        for grid_name in self.grids.keys():
            if grid_name != 'center' and random.random() < self.prob_mutacion:
                grid = individuo[grid_name]
                
                # Elegir subcuadro aleatorio
                i_sub = random.randint(0, 2) * 3
                j_sub = random.randint(0, 2) * 3
                
                # Encontrar celdas mutables
                celdas_mutables = []
                for i in range(3):
                    for j in range(3):
                        if not self.celdas_fijas[grid_name][i_sub + i][j_sub + j]:
                            celdas_mutables.append((i_sub + i, j_sub + j))
                
                if len(celdas_mutables) >= 2:
                    celda1, celda2 = random.sample(celdas_mutables, 2)
                    grid[celda1[0]][celda1[1]], grid[celda2[0]][celda2[1]] = grid[celda2[0]][celda2[1]], grid[celda1[0]][celda1[1]]
        
        return individuo
    
    def copiar_individuo(self, individuo):
        """Copia profunda de un individuo"""
        copia = {}
        for grid_name, grid in individuo.items():
            copia[grid_name] = self.copiar_grid(grid)
        return copia
    
    def ejecutar(self, generaciones=100):
        """Ejecuta el algoritmo genético"""
        print("🧩 Iniciando algoritmo genético...")
        start_time = time.time()
        
        poblacion = self.inicializar_poblacion()
        mejor_fitness = float('-inf')
        mejor_individuo = None
        
        for generacion in range(generaciones):
            fitness_poblacion = [self.calcular_fitness(ind) for ind in poblacion]
            max_fitness = max(fitness_poblacion)
            
            if max_fitness > mejor_fitness:
                mejor_fitness = max_fitness
                mejor_individuo = self.copiar_individuo(poblacion[fitness_poblacion.index(max_fitness)])
            
            if mejor_fitness == 0:
                print(f"🎉 Solución encontrada en generación {generacion}!")
                break
            
            # Crear nueva población
            nueva_poblacion = [self.copiar_individuo(mejor_individuo)]
            
            while len(nueva_poblacion) < self.tam_poblacion:
                padre1, padre2 = self.seleccionar_padres(poblacion, fitness_poblacion)
                hijo = self.cruzar(padre1, padre2)
                hijo = self.mutar(hijo)
                nueva_poblacion.append(hijo)
            
            poblacion = nueva_poblacion
            
            if generacion % 10 == 0:
                elapsed = time.time() - start_time
                print(f"⏳ Gen {generacion}: Fitness = {mejor_fitness} | Tiempo: {elapsed:.2f}s")
        
        elapsed = time.time() - start_time
        print(f"✅ Tiempo total: {elapsed:.2f}s")
        return mejor_individuo, mejor_fitness
    
    def visualizar_grid(self, grid, nombre):
        """Visualiza un grid individual"""
        print(f"\n🔷 {nombre}:")
        print("+" + "---+" * 9)
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("+" + "---+" * 9)
            fila = "|"
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    fila += " |"
                fila += f" {grid[i][j] if grid[i][j] != 0 else '.'} "
            fila += " |"
            print(fila)
        print("+" + "---+" * 9)
    
    def visualizar_solucion(self, individuo):
        """Visualiza la solución completa"""
        print("\n" + "="*60)
        print("🎯 SOLUCIÓN DEL CROSS SUDOKU")
        print("="*60)
        
        self.visualizar_grid(individuo['top'], "Grid Superior")
        print("\n🔄 Grids Interconectados:")
        
        # Mostrar grids izquierdo, central y derecho en paralelo
        print("Left".center(27) + " | " + "Center".center(27) + " | " + "Right".center(27))
        print("-"*85)
        
        for i in range(9):
            fila_izq = " ".join(str(x) if x != 0 else "." for x in individuo['left'][i])
            fila_cen = " ".join(str(x) if x != 0 else "." for x in individuo['center'][i])
            fila_der = " ".join(str(x) if x != 0 else "." for x in individuo['right'][i])
            print(f"{fila_izq.center(27)} | {fila_cen.center(27)} | {fila_der.center(27)}")
        
        self.visualizar_grid(individuo['bottom'], "Grid Inferior")
        print("="*60)

# Ejecutar la simulación
if __name__ == "__main__":
    print("🚀 INICIANDO SIMULACIÓN DE CROSS SUDOKU")
    print("⭐ Este algoritmo generará automáticamente un Cross Sudoku y lo resolverá")
    
    cross_sudoku_solver = CrossSudokuGA(tam_poblacion=100, prob_mutacion=0.2)
    solucion, fitness = cross_sudoku_solver.ejecutar(generaciones=50)
    
    cross_sudoku_solver.visualizar_solucion(solucion)
    print(f"\n📊 Fitness final: {fitness}")
    
    if fitness == 0:
        print("✅ ¡SOLUCIÓN VÁLIDA ENCONTRADA!")
    else:
        print("⚠️  Solución parcial. Ejecute más generaciones para mejorar.")