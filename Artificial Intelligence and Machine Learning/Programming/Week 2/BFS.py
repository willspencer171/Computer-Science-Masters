import sys

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class QueueFrontier:
    def __init__(self):
        self.frontier = []
    
    def add(self, node: Node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    @property
    def isempty(self):
        return len(self.frontier) == 0

    def pop(self):
        if self.isempty:
            raise Exception("Empty Frontier!")
        return self.frontier.pop(0)

class StackFrontier(QueueFrontier):
    def pop(self):
        if self.isempty:
            raise Exception("Empty Frontier!")
        return self.frontier.pop(-1)

class MazeSolver:
    def __init__(self, filename):
        
        with open(filename) as file:
            contents = file.read()
        
        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("Maze must have exactly one goal point")

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == 'A':
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == 'B':
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == ' ':
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            
            self.walls.append(row)
        
        self.solution = None

    def print_solution(self):
        if isinstance(self.frontier, StackFrontier):
            print("Depth-First Search")
        else:
            print("Breadth-First Search")
        states = self.solution[1] if self.solution is not None else None
        actions = " → ".join(self.solution[0]) if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print('█', end='')
                elif (i, j) == self.start:
                    print('A', end='')
                elif (i, j) == self.goal:
                    print('B', end='')
                elif states is not None and (i, j) in states:
                    print('*', end='')
                else:
                    print(' ', end='')
            print()
        print(f"\nNumber of expanded nodes: {self.explored_num}")
        print(f"Actions: {actions}")

    def neighbours(self, state):
        row, col = state

        candidates = [
            ('up', (row - 1, col)),
            ('down', (row + 1, col)),
            ('left', (row, col - 1)),
            ('right', (row, col + 1))
        ]

        result = []

        for action, (r, c) in candidates:
            try:
                if not self.walls[r][c]:
                    result.append((action, (r, c)))
            except IndexError:
                continue
        return result

    def solve(self):
        '''Solves maze problem using either DFS or BFS'''

        # Keep track of explored states
        self.explored_num = 0

        # Initialise starting node and frontier
        start = Node(self.start, None, None)
        # Stack - DFS, Queue - BFS
        self.frontier = QueueFrontier()
        self.frontier.add(start)

        # Initialise empty explored set
        self.explored = set()

        # Loop until solution is found
        while True:
            # Empty frontier only occurs if there are no more moves
            if self.frontier.isempty:
                raise Exception("No solution found")
            
            node = self.frontier.pop()
            self.explored_num += 1

            # if we find the goal state, backtrack to find route
            if node.state == self.goal:
                actions = []
                cells = []

                while node.parent:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            
            self.explored.add(node.state)

            for action, state in self.neighbours(node.state):
                if not self.frontier.contains_state(state) and state not in self.explored:
                    child = Node(state, node, action)
                    self.frontier.add(child)

if __name__ == '__main__':
    maze = MazeSolver(sys.argv[1])
    maze.solve()
    maze.print_solution()
