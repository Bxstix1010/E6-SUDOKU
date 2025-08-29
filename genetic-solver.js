class SudokuGeneticSolver {
    constructor(grid, size = 9) {
        this.grid = grid;
        this.size = size;
        this.populationSize = 500; // Reducido para mejor rendimiento
        this.mutationRate = 0.15;
        this.maxGenerations = 5000;
        this.population = [];
        this.bestSolution = null;
        this.bestFitness = -Infinity;
        this.onGeneration = null;
        this.isPaused = false;
        this.shouldStop = false;
        this.generationCount = 0;
        
        // Precalcular posiciones de celdas vacías
        this.emptyCells = this.findEmptyCells();
    }

    // Encontrar todas las celdas vacías
    findEmptyCells() {
        const empty = [];
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                if (this.grid[i][j] === 0) {
                    empty.push({ row: i, col: j });
                }
            }
        }
        return empty;
    }

    // Inicializar población corregida
    initializePopulation() {
        this.population = [];
        for (let i = 0; i < this.populationSize; i++) {
            const individual = this.createValidIndividual();
            this.population.push(individual);
        }
    }

    // Crear individuo válido (asegurar subcuadrículas válidas)
    createValidIndividual() {
        const individual = JSON.parse(JSON.stringify(this.grid));
        
        // Llenar cada subcuadrícula 3x3 con números válidos
        for (let startRow = 0; startRow < this.size; startRow += 3) {
            for (let startCol = 0; startCol < this.size; startCol += 3) {
                this.fillSubgridWithValidNumbers(individual, startRow, startCol);
            }
        }
        
        return individual;
    }

    // Llenar subcuadrícula con números válidos
    fillSubgridWithValidNumbers(individual, startRow, startCol) {
        const usedNumbers = new Set();
        const emptyPositions = [];
        
        // Identificar números usados y posiciones vacías
        for (let i = startRow; i < startRow + 3; i++) {
            for (let j = startCol; j < startCol + 3; j++) {
                if (individual[i][j] !== 0) {
                    usedNumbers.add(individual[i][j]);
                } else {
                    emptyPositions.push({ row: i, col: j });
                }
            }
        }
        
        // Generar números faltantes
        const missingNumbers = [];
        for (let num = 1; num <= 9; num++) {
            if (!usedNumbers.has(num)) {
                missingNumbers.push(num);
            }
        }
        
        // Mezclar y asignar números faltantes
        this.shuffleArray(missingNumbers);
        for (let idx = 0; idx < emptyPositions.length; idx++) {
            const pos = emptyPositions[idx];
            individual[pos.row][pos.col] = missingNumbers[idx];
        }
    }

    // Función de fitness mejorada
    calculateFitness(individual) {
        let fitness = 1000; // Fitness base
        
        // Penalizar duplicados en filas
        for (let i = 0; i < this.size; i++) {
            const rowSet = new Set();
            for (let j = 0; j < this.size; j++) {
                rowSet.add(individual[i][j]);
            }
            fitness -= (this.size - rowSet.size) * 10;
        }
        
        // Penalizar duplicados en columnas
        for (let j = 0; j < this.size; j++) {
            const colSet = new Set();
            for (let i = 0; i < this.size; i++) {
                colSet.add(individual[i][j]);
            }
            fitness -= (this.size - colSet.size) * 10;
        }
        
        // Bonificación por subcuadrículas válidas (ya lo son por construcción)
        fitness += 50;
        
        return fitness;
    }

    // Selección por ruleta (más efectiva)
    rouletteSelection() {
        const totalFitness = this.population.reduce((sum, ind) => sum + this.calculateFitness(ind), 0);
        let random = Math.random() * totalFitness;
        
        for (const individual of this.population) {
            random -= this.calculateFitness(individual);
            if (random <= 0) {
                return individual;
            }
        }
        
        return this.population[this.population.length - 1];
    }

    // Cruzamiento mejorado
    crossover(parent1, parent2) {
        const child = JSON.parse(JSON.stringify(this.grid));
        
        // Cruzamiento por punto aleatorio
        const crossoverPoint = Math.floor(Math.random() * this.emptyCells.length);
        
        for (let i = 0; i < this.emptyCells.length; i++) {
            const cell = this.emptyCells[i];
            if (i < crossoverPoint) {
                child[cell.row][cell.col] = parent1[cell.row][cell.col];
            } else {
                child[cell.row][cell.col] = parent2[cell.row][cell.col];
            }
        }
        
        return child;
    }

    // Mutación mejorada
    mutate(individual) {
        if (Math.random() < this.mutationRate) {
            // Seleccionar una subcuadrícula aleatoria
            const subgridRow = Math.floor(Math.random() * 3) * 3;
            const subgridCol = Math.floor(Math.random() * 3) * 3;
            
            // Encontrar dos celdas mutables en la misma subcuadrícula
            const mutableCells = [];
            for (let i = subgridRow; i < subgridRow + 3; i++) {
                for (let j = subgridCol; j < subgridCol + 3; j++) {
                    if (this.grid[i][j] === 0) { // Solo celdas que originalmente estaban vacías
                        mutableCells.push({ row: i, col: j });
                    }
                }
            }
            
            if (mutableCells.length >= 2) {
                // Seleccionar dos celdas aleatorias
                const [cell1, cell2] = this.selectRandomCells(mutableCells, 2);
                
                // Intercambiar valores
                [individual[cell1.row][cell1.col], individual[cell2.row][cell2.col]] = 
                [individual[cell2.row][cell2.col], individual[cell1.row][cell1.col]];
            }
        }
        
        return individual;
    }

    // Evolución de la población
    evolve() {
        const newPopulation = [];
        
        // Elitismo: mantener el mejor individuo
        if (this.bestSolution) {
            newPopulation.push(JSON.parse(JSON.stringify(this.bestSolution)));
        }
        
        // Llenar el resto de la población
        while (newPopulation.length < this.populationSize) {
            const parent1 = this.rouletteSelection();
            const parent2 = this.rouletteSelection();
            
            let child = this.crossover(parent1, parent2);
            child = this.mutate(child);
            
            newPopulation.push(child);
        }
        
        this.population = newPopulation;
    }

    // Resolver el sudoku (corregido)
    async solve() {
        console.log("🧬 Iniciando algoritmo genético...");
        this.shouldStop = false;
        this.generationCount = 0;
        
        this.initializePopulation();
        
        for (let generation = 0; generation < this.maxGenerations; generation++) {
            this.generationCount = generation;
            
            // Manejar pausa
            while (this.isPaused && !this.shouldStop) {
                await new Promise(resolve => setTimeout(resolve, 100));
            }
            if (this.shouldStop) break;
            
            // Evaluar población
            let bestGenFitness = -Infinity;
            let bestGenSolution = null;
            let foundPerfectSolution = false;
            
            for (const individual of this.population) {
                const fitness = this.calculateFitness(individual);
                
                if (fitness > bestGenFitness) {
                    bestGenFitness = fitness;
                    bestGenSolution = JSON.parse(JSON.stringify(individual));
                }
                
                // Verificar si es solución perfecta
                if (this.isPerfectSolution(individual)) {
                    console.log(`✅ Solución perfecta encontrada en generación ${generation}`);
                    foundPerfectSolution = true;
                    bestGenSolution = individual;
                    bestGenFitness = 1000; // Fitness perfecto
                    break;
                }
            }
            
            // Actualizar mejor solución global
            if (bestGenFitness > this.bestFitness) {
                this.bestFitness = bestGenFitness;
                this.bestSolution = bestGenSolution;
            }
            
            // Notificar progreso
            if (this.onGeneration) {
                this.onGeneration({
                    generation,
                    bestFitness: this.bestFitness,
                    currentFitness: bestGenFitness,
                    bestSolution: this.bestSolution,
                    operation: foundPerfectSolution ? 
                        "¡Solución perfecta encontrada!" : 
                        `Generación ${generation} completada`
                });
            }
            
            // Log cada 50 generaciones
            if (generation % 50 === 0) {
                console.log(`Gen ${generation}: Mejor fitness = ${this.bestFitness}`);
            }
            
            // Terminar si encontramos solución perfecta
            if (foundPerfectSolution) {
                return bestGenSolution;
            }
            
            // Evolucionar si no hemos terminado
            this.evolve();
        }
        
        console.log("⏰ Límite de generaciones alcanzado");
        return this.bestSolution;
    }

    // Verificar si es solución perfecta
    isPerfectSolution(individual) {
        // Verificar filas
        for (let i = 0; i < this.size; i++) {
            const rowSet = new Set(individual[i]);
            if (rowSet.size !== this.size) return false;
        }
        
        // Verificar columnas
        for (let j = 0; j < this.size; j++) {
            const colSet = new Set();
            for (let i = 0; i < this.size; i++) {
                colSet.add(individual[i][j]);
            }
            if (colSet.size !== this.size) return false;
        }
        
        return true;
    }

    // Métodos de control
    pause() { this.isPaused = true; }
    resume() { this.isPaused = false; }
    stop() { this.shouldStop = true; this.isPaused = false; }

    // Utilidades
    shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    selectRandomCells(cells, count) {
        const shuffled = [...cells];
        this.shuffleArray(shuffled);
        return shuffled.slice(0, count);
    }
}