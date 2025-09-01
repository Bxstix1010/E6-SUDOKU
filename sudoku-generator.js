class SudokuGenerator {
    constructor(size = 9) {
        this.size = size;
        this.grid = Array(size).fill().map(() => Array(size).fill(0));
        this.subgridSize = Math.sqrt(size);
    }

    generateComplete() {
        this.grid = Array(this.size).fill().map(() => Array(this.size).fill(0));
        this.solveComplete();
        return this.grid;
    }

    solveComplete() {
        for (let row = 0; row < this.size; row++) {
            for (let col = 0; col < this.size; col++) {
                if (this.grid[row][col] === 0) {
                    const numbers = this.shuffleArray([...Array(this.size).keys()].map(n => n + 1));
                    
                    for (const num of numbers) {
                        if (this.isValidPlacement(row, col, num)) {
                            this.grid[row][col] = num;
                            
                            if (this.solveComplete()) {
                                return true;
                            }
                            
                            this.grid[row][col] = 0;
                        }
                    }
                    return false;
                }
            }
        }
        return true;
    }

    createPuzzle(difficulty) {
        const completeGrid = this.generateComplete();
        const puzzle = JSON.parse(JSON.stringify(completeGrid));
        
        const cellsToRemove = {
            'easy': 35,    // 46 pistas
            'medium': 45,  // 36 pistas  
            'hard': 52,    // 29 pistas
            'expert': 58   // 23 pistas
        }[difficulty] || 45;
        
        this.removeCells(puzzle, cellsToRemove);
        return puzzle;
    }

    removeCells(grid, count) {
        const cells = [];
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                cells.push({row: i, col: j});
            }
        }
        
        this.shuffleArray(cells);
        let removed = 0;
        
        for (const cell of cells) {
            if (removed >= count) break;
            
            const backup = grid[cell.row][cell.col];
            grid[cell.row][cell.col] = 0;
            
            if (this.hasUniqueSolution(JSON.parse(JSON.stringify(grid)))) {
                removed++;
            } else {
                grid[cell.row][cell.col] = backup;
            }
        }
    }

    hasUniqueSolution(grid) {
        const solutions = this.countSolutions(JSON.parse(JSON.stringify(grid)), 0);
        return solutions === 1;
    }

    countSolutions(grid, count) {
        if (count > 1) return count;
        
        for (let row = 0; row < this.size; row++) {
            for (let col = 0; col < this.size; col++) {
                if (grid[row][col] === 0) {
                    for (let num = 1; num <= this.size; num++) {
                        if (this.isValidPlacementForGrid(grid, row, col, num)) {
                            grid[row][col] = num;
                            count = this.countSolutions(grid, count);
                            if (count > 1) return count;
                            grid[row][col] = 0;
                        }
                    }
                    return count;
                }
            }
        }
        return count + 1;
    }

    isValidPlacementForGrid(grid, row, col, num) {
        for (let i = 0; i < this.size; i++) {
            if (grid[row][i] === num) return false;
        }
        
        for (let i = 0; i < this.size; i++) {
            if (grid[i][col] === num) return false;
        }
        
        const startRow = Math.floor(row / this.subgridSize) * this.subgridSize;
        const startCol = Math.floor(col / this.subgridSize) * this.subgridSize;
        
        for (let i = 0; i < this.subgridSize; i++) {
            for (let j = 0; j < this.subgridSize; j++) {
                if (grid[startRow + i][startCol + j] === num) return false;
            }
        }
        
        return true;
    }

    isValidPlacement(row, col, num) {
        return this.isValidPlacementForGrid(this.grid, row, col, num);
    }

    shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }
}