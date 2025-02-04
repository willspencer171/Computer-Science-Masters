from A_star import *
import math
from scipy.spatial import distance

class EightPuzzle(AStarProblem):
    def __init__(self, start):
        goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        self.nrows = int(math.sqrt(len(goal)))
        self.goal_positions = {tile: divmod(i, self.nrows) for i, tile in enumerate(goal)}
        super().__init__(start, goal)

    def neighbours(self, state):
        state = list(state)
        neighbours = []
        blank_index = state.index(0)
        row, col = divmod(blank_index, self.nrows)
        
        actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in actions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.nrows and 0 <= new_col < self.nrows:
                new_index = new_row * self.nrows + new_col
                new_state = state[:]
                new_state[blank_index], new_state[new_index] = new_state[new_index], new_state[blank_index]
                neighbours.append((tuple(new_state), 1))  # Move cost is 1
        return neighbours

    def heuristic(self, state):
        return sum(
            distance.cityblock(divmod(i, self.nrows), self.goal_positions[tile])
            for i, tile in enumerate(state) if tile != 0
        )
    
start_state = (2,3,5,8,7,6,4,1,0)
puzzle = EightPuzzle(start_state)

solution = puzzle.ida_star()

print("Solution:")
if solution is not None:
    for i, step in enumerate(solution):
        step = [str(tile) for tile in step]
        print(" ".join(step[:3]))
        print(" ".join(step[3:6]))
        print(" ".join(step[6:]))
        if i != len(solution) - 1:
            print("↓".center(5))

else:
    print("No solution found")
