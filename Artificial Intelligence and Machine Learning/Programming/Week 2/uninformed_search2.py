from typing import NamedTuple

class LimitException(Exception):
    def __init__(self, limit):
        self.limit = limit
    
    def __str__(self):
        return "No solution found at limit: " + repr(self.limit)

class Node:
    def __init__(self, state, action, parent, z):
        self.parent = parent
        self.state = state
        self.action = action
        self.z = z

class QueueFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node: Node):
        self.frontier.append(node)

    @property
    def isempty(self):
        return len(self.frontier) == 0
    
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def pop(self):
        if not self.isempty:
            return self.frontier.pop(0)
        
class GridSolver:
    def __init__(self, filename):
        with open(filename, encoding='utf') as f:
            contents = f.read()
        
        contents = contents.split('|')
        grids = [grid.splitlines() for grid in contents]

        self.heights = [len(grid) for grid in grids]
        self.widths = [max(len(line) for line in grid) 
                       for grid in grids]
        
        self.starts = []
        self.goals = []
        self.solutions = [] * len(grids)

        self.congestions = []
        for gridno in range(len(grids)):
            congestion = []
            for i in range(self.heights[gridno]):
                row = []
                for j in range(self.widths[gridno]):
                    try:
                        if grids[gridno][i][j] == 'A':
                            self.starts.append((i, j))
                            row.append(False)
                        elif grids[gridno][i][j] == 'B':
                            self.goals.append((i, j))
                            row.append(False)
                        elif grids[gridno][i][j] == ' ':
                            row.append(False)
                        else:
                            row.append(True)
                    except IndexError:
                        continue
                congestion.append(row)
            self.congestions.append(congestion)

    def expand_node(self, node, gridno):
        print(f"Unpacking node at {node.state}")
        (x, y) = node.state 

        candidates = [
            ('up', (x - 1, y)),
            ('down', (x + 1, y)),
            ('left', (x, y - 1)),
            ('right', (x, y + 1))
        ]

        neighbours = []

        for action, (x, y) in candidates:
            try:
                if not self.congestions[gridno][x][y] and \
                    x >= 0 and x < self.widths[gridno] and \
                    y >= 0 and y < self.heights[gridno] and \
                    (x, y) not in self.explored:
                    neighbours.append((action, (x, y)))
            except IndexError:
                continue
        return neighbours
    
    def depth_limited_search(self, limit, gridno):
        self.explored = set()
        start = Node(self.starts[gridno], None, None, 0)
        self.explored.add(start.state)
        return self.recursive_DLS(start, limit, gridno)
    
    def solve(self, gridno):
        limit = 0
        while True:
            limit += 1
            res = self.depth_limited_search(limit, gridno)
            if res != 'cutoff': 
                return res
            else:
                print(f'cutoff at {limit}')

    def recursive_DLS(self, node: Node, limit, gridno, depth=0):
        self.solution_found = False
        # Goal test
        if self.goals[gridno] == node.state:
            print(f"Solution found at depth {depth}!")
            actions = []
            cells = []

            while node.parent:
                actions.append(node.action)
                cells.append(node.state)
                node = node.parent
            
            cells.append(node.state)
            actions.reverse()
            cells.reverse()
            return (actions, cells)

        elif limit == 0:
            return 'cutoff'
        
        cutoff = False

        for action, state in self.expand_node(node, gridno):
            child = Node(state, action, node, node.z + 1)
            self.explored.add(child.state)
            res = self.recursive_DLS(child, limit-1, gridno, depth+1)
            if res == 'cutoff':
                cutoff = True
            elif res != 'failure':
                return res
        
        if cutoff:
            return 'cutoff'
        else:
            return 'failure'

if __name__ =='__main__':
    grid_solve = GridSolver('Programming/Week 2/grids.txt')
    actions, states = grid_solve.solve(0)
    print("Actions:\n\t" + " → ".join(actions))
    print("States:\n\t" + " → ".join([f"({state[0]}, {state[1]})" for state in states]))
