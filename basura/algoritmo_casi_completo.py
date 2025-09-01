import random
import time
from collections import defaultdict
from abc import ABC, abstractmethod

# ==================== CONFIGURACIONES Y CONSTANTES ====================
SUDOKU_TYPES = {
    'subdoku': {'size': 4, 'regions': 2, 'symbols': '1234'},
    'classic': {'size': 9, 'regions': 3, 'symbols': '123456789'},
    'super': {'size': 16, 'regions': 4, 'symbols': '123456789ABCDEFG'},
    'zilla': {'size': 25, 'regions': 5, 'symbols': '123456789ABCDEFGHIJKLMNOP'}
}

SYMBOL_SETS = {
    'numbers': '123456789',
    'letters': 'ABCDEFGHI',
    'symbols': '⭐🔥💧🌪️💫🌟💥🌊🌀',
    'colors': ['🔴', '🟢', '🔵', '🟡', '🟣', '🟠', '⚫', '⚪', '🟤']
}

RULESETS = {
    'classic': ['row_unique', 'col_unique', 'region_unique'],
    'killer': ['classic', 'cage_sum'],
    'samurai': ['classic', 'interconnected'],
    'x_sudoku': ['classic', 'diagonal_unique'],
    'greater_than': ['classic', 'inequality'],
    'consecutive': ['classic', 'consecutive_adjacent'],
    'even_odd': ['classic', 'parity_constraints'],
    'jigsaw': ['classic', 'irregular_regions']
}

DIFFICULTY_LEVELS = {
    'beginner': {'cells_to_remove': 30, 'min_clues': 40, 'hint_penalty': 0.1},
    'easy': {'cells_to_remove': 40, 'min_clues': 35, 'hint_penalty': 0.2},
    'medium': {'cells_to_remove': 50, 'min_clues': 30, 'hint_penalty': 0.3},
    'hard': {'cells_to_remove': 55, 'min_clues': 25, 'hint_penalty': 0.4},
    'expert': {'cells_to_remove': 60, 'min_clues': 20, 'hint_penalty': 0.5}
}

# ==================== CLASES BASE Y ABSTRACTAS ====================
class SudokuGenerator(ABC):
    @abstractmethod
    def generate(self, difficulty):
        pass

class SudokuSolver(ABC):
    @abstractmethod
    def solve(self, grid):
        pass

# ==================== MOTOR PRINCIPAL DE SUDOKU ====================
class SudokuEngine:
    def __init__(self, sudoku_type='classic', symbol_set='numbers', ruleset='classic', difficulty='medium'):
        self.config = {
            'type': sudoku_type,
            'symbols': symbol_set,
            'ruleset': ruleset,
            'difficulty': difficulty
        }
        
        self.size = SUDOKU_TYPES[sudoku_type]['size']
        self.regions = self._generate_regions(sudoku_type)
        self.symbols = SYMBOL_SETS[symbol_set]
        self.rules = RULESETS[ruleset]
        
        self.grid = [[None] * self.size for _ in range(self.size)]
        self.solution = [[None] * self.size for _ in range(self.size)]
        self.fixed_cells = set()
        self.user_input = {}
        self.possible_values = [[list(self.symbols) for _ in range(self.size)] for _ in range(self.size)]
        
        self.start_time = None
        self.elapsed_time = 0
        self.hints_used = 0
        self.errors_made = 0
        self.moves_history = []
        
        self._initialize_game()

    def _generate_regions(self, sudoku_type):
        regions = []
        region_size = SUDOKU_TYPES[sudoku_type]['regions']
        for i in range(0, self.size, region_size):
            for j in range(0, self.size, region_size):
                region = []
                for x in range(region_size):
                    for y in range(region_size):
                        region.append((i + x, j + y))
                regions.append(region)
        return regions

    def _initialize_game(self):
        generator = self._get_generator()
        self.solution = generator.generate(self.config['difficulty'])
        self._create_playable_grid()
        self.start_time = time.time()

    def _get_generator(self):
        if 'killer' in self.rules:
            return KillerSudokuGenerator(self)
        elif 'samurai' in self.rules:
            return SamuraiSudokuGenerator(self)
        elif 'jigsaw' in self.rules:
            return JigsawSudokuGenerator(self)
        else:
            return ClassicSudokuGenerator(self)

    def _create_playable_grid(self):
        difficulty_settings = DIFFICULTY_LEVELS[self.config['difficulty']]
        cells_to_remove = difficulty_settings['cells_to_remove']
        
        self.grid = [row[:] for row in self.solution]
        self.fixed_cells = set()
        
        cells_removed = 0
        while cells_removed < cells_to_remove:
            i, j = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if self.grid[i][j] is not None:
                self.grid[i][j] = None
                cells_removed += 1
            else:
                self.fixed_cells.add((i, j))

    def make_move(self, row, col, value):
        if (row, col) in self.fixed_cells:
            return False, "Cannot modify fixed cell"
        
        if value not in self.symbols:
            return False, "Invalid value"
        
        self.user_input[(row, col)] = value
        self.moves_history.append(('move', row, col, value))
        
        if value != self.solution[row][col]:
            self.errors_made += 1
            return False, "Incorrect move"
        
        return True, "Move accepted"

    def get_hint(self, hint_type='smart'):
        self.hints_used += 1
        hint_system = HintSystem(self)
        return hint_system.get_hint(hint_type)

    def check_solution(self):
        for i in range(self.size):
            for j in range(self.size):
                current_value = self.grid[i][j] if (i, j) not in self.user_input else self.user_input.get((i, j))
                if current_value != self.solution[i][j]:
                    return False
        return True

    def get_elapsed_time(self):
        if self.start_time:
            return time.time() - self.start_time
        return 0

    def get_progress(self):
        filled = sum(1 for i in range(self.size) for j in range(self.size) 
                    if self.grid[i][j] is not None or (i, j) in self.user_input)
        return filled / (self.size * self.size)

# ==================== GENERADORES DE SUDOKU ====================
class ClassicSudokuGenerator(SudokuGenerator):
    def __init__(self, engine):
        self.engine = engine

    def generate(self, difficulty):
        grid = [[None] * self.engine.size for _ in range(self.engine.size)]
        self._solve_grid(grid)
        return grid

    def _solve_grid(self, grid):
        for i in range(self.engine.size):
            for j in range(self.engine.size):
                if grid[i][j] is None:
                    for symbol in random.sample(self.engine.symbols, len(self.engine.symbols)):
                        if self._is_valid(grid, i, j, symbol):
                            grid[i][j] = symbol
                            if self._solve_grid(grid):
                                return True
                            grid[i][j] = None
                    return False
        return True

    def _is_valid(self, grid, row, col, symbol):
        # Check row
        if symbol in grid[row]:
            return False
        
        # Check column
        if symbol in [grid[i][col] for i in range(self.engine.size)]:
            return False
        
        # Check region
        for region in self.engine.regions:
            if (row, col) in region:
                for i, j in region:
                    if grid[i][j] == symbol:
                        return False
                break
        
        return True

class KillerSudokuGenerator(ClassicSudokuGenerator):
    def generate(self, difficulty):
        grid = super().generate(difficulty)
        self._add_killer_cages(grid)
        return grid

    def _add_killer_cages(self, grid):
        # Implementación simplificada de jaulas Killer
        pass

class SamuraiSudokuGenerator(SudokuGenerator):
    def generate(self, difficulty):
        # Implementación simplificada de Samurai Sudoku
        grids = []
        for _ in range(5):
            classic_gen = ClassicSudokuGenerator(self.engine)
            grids.append(classic_gen.generate(difficulty))
        return self._connect_grids(grids)

    def _connect_grids(self, grids):
        # Conectar los 5 grids en forma de samurái
        pass

class JigsawSudokuGenerator(ClassicSudokuGenerator):
    def generate(self, difficulty):
        grid = super().generate(difficulty)
        self._create_irregular_regions()
        return grid

    def _create_irregular_regions(self):
        # Crear regiones de forma irregular
        pass

# ==================== SISTEMA DE RAZONAMIENTO DEDUCTIVO ====================
class DeductiveReasoning:
    def __init__(self, engine):
        self.engine = engine

    def find_naked_singles(self):
        for i in range(self.engine.size):
            for j in range(self.engine.size):
                if self.engine.grid[i][j] is None and (i, j) not in self.engine.user_input:
                    possible = self._get_possible_values(i, j)
                    if len(possible) == 1:
                        return i, j, possible[0]
        return None

    def find_hidden_singles(self):
        for region_type in ['row', 'col', 'region']:
            for index in range(self.engine.size):
                region_cells = self._get_region_cells(region_type, index)
                for symbol in self.engine.symbols:
                    possible_cells = []
                    for i, j in region_cells:
                        if self._get_cell_value(i, j) is None and symbol in self._get_possible_values(i, j):
                            possible_cells.append((i, j))
                    if len(possible_cells) == 1:
                        return possible_cells[0][0], possible_cells[0][1], symbol
        return None

    def _get_possible_values(self, row, col):
        impossible = set()
        
        # Check row and column
        for i in range(self.engine.size):
            if self._get_cell_value(row, i) is not None:
                impossible.add(self._get_cell_value(row, i))
            if self._get_cell_value(i, col) is not None:
                impossible.add(self._get_cell_value(i, col))
        
        # Check region
        for region in self.engine.regions:
            if (row, col) in region:
                for i, j in region:
                    if self._get_cell_value(i, j) is not None:
                        impossible.add(self._get_cell_value(i, j))
                break
        
        return [s for s in self.engine.symbols if s not in impossible]

    def _get_cell_value(self, row, col):
        if (row, col) in self.engine.user_input:
            return self.engine.user_input[(row, col)]
        return self.engine.grid[row][col]

    def _get_region_cells(self, region_type, index):
        if region_type == 'row':
            return [(index, j) for j in range(self.engine.size)]
        elif region_type == 'col':
            return [(i, index) for i in range(self.engine.size)]
        else:  # region
            return self.engine.regions[index]

# ==================== SISTEMA DE PISTAS INTELIGENTES ====================
class HintSystem:
    def __init__(self, engine):
        self.engine = engine
        self.deductive = DeductiveReasoning(engine)

    def get_hint(self, hint_type='smart'):
        hint_methods = {
            'basic': self._basic_hint,
            'region': self._region_hint,
            'technique': self._technique_hint,
            'smart': self._smart_hint,
            'solution': self._solution_hint
        }
        
        return hint_methods[hint_type]()

    def _basic_hint(self):
        for i in range(self.engine.size):
            for j in range(self.engine.size):
                if self.engine.grid[i][j] is None and (i, j) not in self.engine.user_input:
                    return f"Try filling cell ({i+1}, {j+1})"
        return "No basic hints available"

    def _smart_hint(self):
        # Naked singles
        naked_single = self.deductive.find_naked_singles()
        if naked_single:
            return f"Naked single: Cell ({naked_single[0]+1}, {naked_single[1]+1}) must be {naked_single[2]}"
        
        # Hidden singles
        hidden_single = self.deductive.find_hidden_singles()
        if hidden_single:
            return f"Hidden single: Cell ({hidden_single[0]+1}, {hidden_single[1]+1}) must be {hidden_single[2]}"
        
        return self._technique_hint()

    def _technique_hint(self):
        techniques = [
            "Check for naked pairs in rows",
            "Look for hidden pairs in columns",
            "Try elimination in the current region",
            "Check for unique possibilities in each 3x3 block"
        ]
        return random.choice(techniques)

    def _region_hint(self):
        regions = ['top-left', 'top-right', 'center', 'bottom-left', 'bottom-right']
        return f"Focus on the {random.choice(regions)} region"

    def _solution_hint(self):
        for i in range(self.engine.size):
            for j in range(self.engine.size):
                if self.engine.grid[i][j] is None and (i, j) not in self.engine.user_input:
                    return f"Cell ({i+1}, {j+1}) should be {self.engine.solution[i][j]}"
        return "Puzzle already solved"

# ==================== SISTEMA DE VALIDACIÓN ====================
class SudokuValidator:
    def __init__(self, engine):
        self.engine = engine

    def validate_grid(self):
        errors = []
        
        # Validate rows
        for i in range(self.engine.size):
            if not self._validate_region([(i, j) for j in range(self.engine.size)]):
                errors.append(f"Row {i+1} has duplicates")
        
        # Validate columns
        for j in range(self.engine.size):
            if not self._validate_region([(i, j) for i in range(self.engine.size)]):
                errors.append(f"Column {j+1} has duplicates")
        
        # Validate regions
        for idx, region in enumerate(self.engine.regions):
            if not self._validate_region(region):
                errors.append(f"Region {idx+1} has duplicates")
        
        return errors

    def _validate_region(self, cells):
        values = []
        for i, j in cells:
            value = self.engine.user_input.get((i, j), self.engine.grid[i][j])
            if value is not None:
                if value in values:
                    return False
                values.append(value)
        return True

# ==================== SISTEMA DE ANÁLISIS Y MÉTRICAS ====================
class AnalyticsSystem:
    def __init__(self, engine):
        self.engine = engine
        self.metrics = {
            'completion_time': 0,
            'errors_made': 0,
            'hints_used': 0,
            'moves_count': 0,
            'techniques_used': defaultdict(int),
            'difficulty_level': engine.config['difficulty']
        }

    def update_metrics(self):
        self.metrics['errors_made'] = self.engine.errors_made
        self.metrics['hints_used'] = self.engine.hints_used
        self.metrics['moves_count'] = len(self.engine.moves_history)
        self.metrics['completion_time'] = self.engine.get_elapsed_time()

    def generate_report(self):
        self.update_metrics()
        
        report = {
            'general_stats': {
                'time_spent': self._format_time(self.metrics['completion_time']),
                'total_errors': self.metrics['errors_made'],
                'hints_used': self.metrics['hints_used'],
                'completion_percentage': round(self.engine.get_progress() * 100, 2)
            },
            'performance_metrics': {
                'error_rate': round(self.metrics['errors_made'] / max(1, self.metrics['moves_count']), 3),
                'hint_dependency': round(self.metrics['hints_used'] / max(1, self.metrics['moves_count']), 3),
                'efficiency_score': self._calculate_efficiency_score()
            },
            'suggestions': self._generate_suggestions()
        }
        
        return report

    def _format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def _calculate_efficiency_score(self):
        base_score = 100
        base_score -= self.metrics['errors_made'] * 5
        base_score -= self.metrics['hints_used'] * 10
        base_score -= min(50, self.metrics['completion_time'] / 60)  # Penalize time over 50 minutes
        return max(0, base_score)

    def _generate_suggestions(self):
        suggestions = []
        
        if self.metrics['errors_made'] > 10:
            suggestions.append("Practice more careful number placement to reduce errors")
        
        if self.metrics['hints_used'] > 5:
            suggestions.append("Try to solve more independently before using hints")
        
        if self.metrics['completion_time'] > 1800:  # 30 minutes
            suggestions.append("Work on improving your solving speed with practice")
        
        if not suggestions:
            suggestions.append("Great job! Keep practicing to maintain your skills")
        
        return suggestions

# ==================== API PRINCIPAL DEL SISTEMA ====================
class MultiSudokuSystem:
    def __init__(self):
        self.current_game = None
        self.saved_games = {}
        self.analytics = {}

    def start_new_game(self, sudoku_type='classic', symbol_set='numbers', 
                      ruleset='classic', difficulty='medium'):
        self.current_game = SudokuEngine(sudoku_type, symbol_set, ruleset, difficulty)
        return True, "New game started"

    def make_move(self, row, col, value):
        if not self.current_game:
            return False, "No active game"
        
        success, message = self.current_game.make_move(row, col, value)
        if success and self.current_game.check_solution():
            return True, "Puzzle completed successfully!"
        
        return success, message

    def get_hint(self, hint_type='smart'):
        if not self.current_game:
            return "No active game"
        
        return self.current_game.get_hint(hint_type)

    def get_game_state(self):
        if not self.current_game:
            return None
        
        return {
            'grid': self.current_game.grid,
            'user_input': self.current_game.user_input,
            'fixed_cells': self.current_game.fixed_cells,
            'elapsed_time': self.current_game.get_elapsed_time(),
            'progress': self.current_game.get_progress()
        }

    def validate_solution(self):
        if not self.current_game:
            return False, "No active game"
        
        validator = SudokuValidator(self.current_game)
        errors = validator.validate_grid()
        
        if errors:
            return False, f"Found {len(errors)} errors: {', '.join(errors[:3])}"
        
        return True, "Solution is valid"

    def get_analytics(self):
        if not self.current_game:
            return None
        
        analytics = AnalyticsSystem(self.current_game)
        return analytics.generate_report()

    def save_game(self, game_id):
        if not self.current_game:
            return False, "No active game to save"
        
        self.saved_games[game_id] = {
            'config': self.current_game.config,
            'grid': self.current_game.grid,
            'user_input': self.current_game.user_input,
            'elapsed_time': self.current_game.get_elapsed_time()
        }
        
        return True, f"Game saved as {game_id}"

    def load_game(self, game_id):
        if game_id not in self.saved_games:
            return False, "Game not found"
        
        saved = self.saved_games[game_id]
        self.current_game = SudokuEngine(
            saved['config']['type'],
            saved['config']['symbols'],
            saved['config']['ruleset'],
            saved['config']['difficulty']
        )
        
        self.current_game.grid = saved['grid']
        self.current_game.user_input = saved['user_input']
        self.current_game.start_time = time.time() - saved['elapsed_time']
        
        return True, "Game loaded successfully"

# ==================== EJEMPLO DE USO ====================
def main():
    # Crear el sistema multi-sudoku
    sudoku_system = MultiSudokuSystem()
    
    # Iniciar un nuevo juego clásico
    success, message = sudoku_system.start_new_game(
        sudoku_type='classic',
        symbol_set='numbers',
        ruleset='classic',
        difficulty='medium'
    )
    
    print(message)
    
    # Obtener estado del juego
    game_state = sudoku_system.get_game_state()
    print(f"Progress: {game_state['progress']:.1%}")
    print(f"Elapsed time: {game_state['elapsed_time']:.2f} seconds")
    
    # Pedir una pista inteligente
    hint = sudoku_system.get_hint('smart')
    print(f"Hint: {hint}")
    
    # Intentar hacer un movimiento
    success, message = sudoku_system.make_move(0, 0, '5')
    print(f"Move result: {message}")
    
    # Obtener analytics
    analytics = sudoku_system.get_analytics()
    print("\nAnalytics Report:")
    print(f"Time spent: {analytics['general_stats']['time_spent']}")
    print(f"Errors made: {analytics['general_stats']['total_errors']}")
    print(f"Completion: {analytics['general_stats']['completion_percentage']}%")
    
    # Validar solución
    valid, validation_msg = sudoku_system.validate_solution()
    print(f"Validation: {validation_msg}")

if __name__ == "__main__":
    main()