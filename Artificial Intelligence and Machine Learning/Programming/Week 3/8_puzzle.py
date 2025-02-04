from A_star import *
from scipy.spatial import distance

class EightPuzzle(AStarProblem):
    def __init__(self, start):
        goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        super().__init__(start, goal)

    def neighbours(self, state):
        state = list(state)
        neighbours = []
        blank_index = state.index(0)
        row, col = divmod(blank_index, 3)
        
        actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in actions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_index = new_row * 3 + new_col
                new_state = state[:]
                new_state[blank_index], new_state[new_index] = new_state[new_index], new_state[blank_index]
                neighbours.append((tuple(new_state), 1))  # Move cost is 1
        return neighbours

    def heuristic(self, state):
        total_dist = 0
        for i, tile in enumerate(state):
            if tile == 0:
                continue
            goal_index = self.goal.index(tile)
            total_dist += distance.cityblock(divmod(i, 3), divmod(goal_index, 3))
        return total_dist
    
start_state = (2,5,4,3,6,0,1,7,8)
puzzle = EightPuzzle(start_state)

solution = puzzle.astar()

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
