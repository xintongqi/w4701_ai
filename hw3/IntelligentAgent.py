"""
Amy QI, xq2224
"""

from BaseAI import BaseAI
import time

class IntelligentAgent(BaseAI):
    start_time = 0
    time_allowed = 0.2
    depth_allowed = 4

    smooth_weight = 0.1
    monotonicity_weight = 1
    empty_weight = 1
    snake_weight = 0.5

    defaultProbability = 0.9

    snake_weights = [[40, 20, 10, 5],
                     [15, 10, 5, 2],
                     [10, 5, 2, 1],
                     [2, 2, 1, 0.5]]

    def __init__(self):
        pass

    def heuristic_smoothness(self, grid):
        smoothness = 0
        for row in grid.map:
            for i in range(len(row) - 1):
                smoothness += abs(row[i] - row[i + 1])
        for col in list(zip(*grid.map)):
            for i in range(len(col) - 1):
                smoothness += abs(col[i] - col[i + 1])
        return smoothness

    def heuristic_monotonicity(self, grid):
        monotonicity = 0
        for row in grid.map:
            for i in range(len(row) - 1):
                if row[i] >= row[i + 1]:
                    monotonicity += 1
        for col in list(zip(*grid.map)):
            for i in range(len(col) - 1):
                if col[i] >= col[i + 1]:
                    monotonicity += 1
        return monotonicity

    def heuristic_snake(self, grid):
        snake = 0
        for row in range(len(grid.map)):
            for col in range(len(grid.map[row])):
                snake += self.snake_weights[col][row] * grid.map[row][col]
        return snake

    def heuristic(self, grid):
        smoothness = self.heuristic_smoothness(grid)
        monotonicity = self.heuristic_monotonicity(grid)
        empty = len(grid.getAvailableCells())
        snake = self.heuristic_snake(grid)
        return empty * self.empty_weight + smoothness * self.smooth_weight + monotonicity * self.monotonicity_weight + snake * self.snake_weight

    def expectmax(self, grid, depth, alpha, beta):
        if depth > self.depth_allowed or time.process_time() - self.start_time > self.time_allowed:
            return self.heuristic(grid), None

        max_val = -float('inf')
        best_move = None

        for move in grid.getAvailableMoves():
            val = self.expectchance(move[1], depth + 1, alpha, beta)
            if val > max_val:
                max_val = val
                best_move = move[0]
            if max_val >= beta:
                return max_val, best_move
            alpha = max(alpha, max_val)

        return max_val, best_move

    def expectchance(self, grid, depth, alpha, beta) -> float:
        if depth > self.depth_allowed or time.process_time() - self.start_time > self.time_allowed:
            return self.heuristic(grid)

        left = self.defaultProbability * self.expectmin(grid, depth + 1, alpha, beta, 2)
        right = (1-self.defaultProbability) * self.expectmin(grid, depth + 1, alpha, beta, 4)
        return (left + right) / 2

    def expectmin(self, grid, depth, alpha, beta, tile_value) -> float:
        if depth > self.depth_allowed or time.process_time() - self.start_time > self.time_allowed:
            return self.heuristic(grid)

        min_val = float('inf')

        for cell in grid.getAvailableCells():
            new_grid = grid.clone()
            new_grid.insertTile(cell, tile_value)
            val, move = self.expectmax(new_grid, depth + 1, alpha, beta)
            min_val = min(min_val, val)
            if min_val <= alpha:
                return min_val
            beta = min(beta, min_val)

        return min_val

    def expectiminimax(self, grid, depth, alpha, beta):
        return self.expectmax(grid, depth, alpha, beta)

    def getMove(self, grid):
        self.start_time = time.process_time()
        best_val, best_move = self.expectiminimax(grid, 0, -float('inf'), float('inf'))

        if best_move is None:
            best_move = grid.getAvailableMoves()[0][0]
            return best_move
        else:
            return best_move
