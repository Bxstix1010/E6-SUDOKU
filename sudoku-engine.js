class SudokuEngine {
    // ... (código anterior保持不变) ...

    async solveWithGeneticAlgorithm(sudokuGrid) {
        try {
            this.showGeneticMonitor();
            this.fitnessHistory = [];
            
            const matrix = this.gridToMatrix(sudokuGrid);
            
            // Verificar que el sudoku tenga solución
            if (!this.isValidPuzzle(matrix)) {
                alert('❌ El sudoku no es válido o no tiene solución');
                this.hideGeneticMonitor();
                return false;
            }
            
            this.solver = new SudokuGeneticSolver(matrix);
            
            this.solver.onGeneration = (data) => {
                this.updateGeneticMonitor(data);
            };

            const solution = await this.solver.solve();
            
            if (solution && this.isPerfectSolution(solution)) {
                this.matrixToGrid(solution, sudokuGrid);
                this.hideGeneticMonitor();
                return true;
            } else {
                this.hideGeneticMonitor();
                alert('⚠️ No se encontró solución perfecta. Mostrando mejor intento...');
                if (solution) {
                    this.matrixToGrid(solution, sudokuGrid);
                }
                return false;
            }
            
        } catch (error) {
            console.error('Error en algoritmo genético:', error);
            this.hideGeneticMonitor();
            alert('❌ Error en el algoritmo genético: ' + error.message);
            return false;
        }
    }

    // Verificar si el puzzle es válido
    isValidPuzzle(matrix) {
        const size = matrix.length;
        
        // Verificar números inválidos
        for (let i = 0; i < size; i++) {
            for (let j = 0; j < size; j++) {
                const num = matrix[i][j];
                if (num < 0 || num > 9) return false;
            }
        }
        
        // Verificar conflictos en números fijos
        for (let i = 0; i < size; i++) {
            for (let j = 0; j < size; j++) {
                const num = matrix[i][j];
                if (num !== 0) {
                    // Verificar fila
                    for (let k = 0; k < size; k++) {
                        if (k !== j && matrix[i][k] === num) return false;
                    }
                    // Verificar columna
                    for (let k = 0; k < size; k++) {
                        if (k !== i && matrix[k][j] === num) return false;
                    }
                    // Verificar subcuadrícula
                    const startRow = Math.floor(i / 3) * 3;
                    const startCol = Math.floor(j / 3) * 3;
                    for (let x = startRow; x < startRow + 3; x++) {
                        for (let y = startCol; y < startCol + 3; y++) {
                            if (x !== i && y !== j && matrix[x][y] === num) return false;
                        }
                    }
                }
            }
        }
        
        return true;
    }

    // Verificar solución perfecta
    isPerfectSolution(matrix) {
        const size = matrix.length;
        
        for (let i = 0; i < size; i++) {
            const rowSet = new Set();
            const colSet = new Set();
            
            for (let j = 0; j < size; j++) {
                // Verificar filas
                if (matrix[i][j] === 0 || rowSet.has(matrix[i][j])) return false;
                rowSet.add(matrix[i][j]);
                
                // Verificar columnas
                if (matrix[j][i] === 0 || colSet.has(matrix[j][i])) return false;
                colSet.add(matrix[j][i]);
            }
        }
        
        // Verificar subcuadrículas
        for (let i = 0; i < size; i += 3) {
            for (let j = 0; j < size; j += 3) {
                const subgridSet = new Set();
                for (let x = i; x < i + 3; x++) {
                    for (let y = j; y < j + 3; y++) {
                        if (matrix[x][y] === 0 || subgridSet.has(matrix[x][y])) return false;
                        subgridSet.add(matrix[x][y]);
                    }
                }
            }
        }
        
        return true;
    }

    // ... (resto del código保持不变) ...
}