class SudokuKnowledgeBase {
    constructor() {
        this.rules = {
            'classic': this.classicRules,
            'killer': this.killerRules,
            'x-sudoku': this.xSudokuRules,
            'samurai': this.samuraiRules,
            'jigsaw': this.jigsawRules
        };
    }

    classicRules(grid) {
        return true; // Reglas básicas ya validadas previamente
    }

    killerRules(grid, cages) {
        for (const cage of cages) {
            let sum = 0;
            const numbers = new Set();
            
            for (const cell of cage.cells) {
                const value = grid[cell.row][cell.col];
                if (value === 0) continue;
                
                sum += value;
                if (numbers.has(value)) return false;
                numbers.add(value);
            }
            
            if (sum > cage.sum) return false;
        }
        return true;
    }

    xSudokuRules(grid) {
        const size = grid.length;
        const mainDiag = new Set();
        const antiDiag = new Set();
        
        for (let i = 0; i < size; i++) {
            if (grid[i][i] !== 0) {
                if (mainDiag.has(grid[i][i])) return false;
                mainDiag.add(grid[i][i]);
            }
            
            if (grid[i][size-1-i] !== 0) {
                if (antiDiag.has(grid[i][size-1-i])) return false;
                antiDiag.add(grid[i][size-1-i]);
            }
        }
        
        return true;
    }

    samuraiRules(grid) {
        // Lógica específica para Samurai Sudoku
        return true;
    }

    jigsawRules(grid) {
        // Lógica específica para Jigsaw Sudoku
        return true;
    }

    validateSolution(grid, gameType, extraData = null) {
        if (!this.rules[gameType]) return false;
        return this.rules[gameType](grid, extraData);
    }
}