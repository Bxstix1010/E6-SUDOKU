class SudokuEngine {
    constructor() {
        this.knowledgeBase = new SudokuKnowledgeBase();
        this.generator = new SudokuGenerator();
        // ... resto del código existente
    }

    // REEMPLAZA la función isValidPuzzle existente con esta:
    isValidPuzzle(matrix, gameType = 'classic', extraData = null) {
        const size = matrix.length;
        
        // Verificación básica
        for (let i = 0; i < size; i++) {
            for (let j = 0; j < size; j++) {
                const num = matrix[i][j];
                if (num < 0 || num > 9) return false;
                if (num !== 0 && !this.isValidBasicPlacement(matrix, i, j, num)) {
                    return false;
                }
            }
        }
        
        // Verificación específica del tipo
        return this.knowledgeBase.validateSolution(matrix, gameType, extraData);
    }

    // AGREGA esta nueva función:
    isValidBasicPlacement(matrix, row, col, num) {
        const size = matrix.length;
        
        // Verificar fila
        for (let i = 0; i < size; i++) {
            if (i !== col && matrix[row][i] === num) return false;
        }
        
        // Verificar columna
        for (let i = 0; i < size; i++) {
            if (i !== row && matrix[i][col] === num) return false;
        }
        
        // Verificar subcuadrícula
        const subgridSize = Math.sqrt(size);
        const startRow = Math.floor(row / subgridSize) * subgridSize;
        const startCol = Math.floor(col / subgridSize) * subgridSize;
        
        for (let i = startRow; i < startRow + subgridSize; i++) {
            for (let j = startCol; j < startCol + subgridSize; j++) {
                if (i !== row && j !== col && matrix[i][j] === num) return false;
            }
        }
        
        return true;
    }

    // AGREGA esta función para generar puzzles:
    generatePuzzle(gameType, difficulty) {
        try {
            return this.generator.createPuzzle(difficulty);
        } catch (error) {
            console.error('Error generating puzzle:', error);
            // Fallback a puzzle predefinido
            return this.getPredefinedPuzzle(difficulty);
        }
    }

    getPredefinedPuzzle(difficulty) {
        // Puzzles predefinidos de respaldo
        const puzzles = {
            'easy': [
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9]
            ],
            'medium': [
                // Agrega puzzle medio aquí
            ]
            // Agrega más dificultades
        };
        
        return JSON.parse(JSON.stringify(puzzles[difficulty] || puzzles.easy));
    }


isValidPuzzle(matrix) {
    const size = matrix.length;
    
    // Verificar números inválidos
    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            const num = matrix[i][j];
            if (num < 0 || num > 9) return false;
            if (num !== 0) {
                // Verificar conflicto en fila
                for (let k = 0; k < size; k++) {
                    if (k !== j && matrix[i][k] === num) return false;
                }
                // Verificar conflicto en columna
                for (let k = 0; k < size; k++) {
                    if (k !== i && matrix[k][j] === num) return false;
                }
                // Verificar conflicto en subcuadrícula 3x3
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

isPerfectSolution(matrix) {
    const size = matrix.length;
    
    // Verificar filas y columnas
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
    
    // Verificar subcuadrículas 3x3
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
}
