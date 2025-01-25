from uninformed_search1 import Node, StackFrontier, QueueFrontier
import csv

class VacuumWorldSolver:
    def __init__(self, filename):
        with open(filename) as f:
            reader = csv.reader(f)
            contents = [row for row in reader]
            headers = contents.pop(0)

        self.frontier = StackFrontier()
        self.solution = None

        self.goals = [7, 8]
    
    def neighbours(self, state):
        int_state = int(state)
        suck_states = [3,6,3,8,7,6,7,8]

        candidate_actions = [
            ('left', (state if int_state % 2 == 1 else int_state - 1)),
            ('right', (state if int_state % 2 == 0 else int_state + 1)),
            ('suck', suck_states[int_state-1]) 
        ]
        neighbours = []
        for action, res in candidate_actions:
            if res != state:
                neighbours.append((action, res))
        
        return neighbours
    
    def print_solution(self):
        if not self.solution:
            raise Exception ("No solution!")
        
        print(f"\n\tPath from state 1 to goal state {self.solution[1][-1]}:\n")
        print(" → ".join([str(val) for val in self.solution[0]]))

    def solve(self):
        start = Node('1', None, None)
        self.frontier.add(start)

        self.explored = set()

        while True:
            if self.frontier.isempty:
                raise Exception("No solution found!")
            
            node = self.frontier.pop()

            if node.state in self.goals:
                actions = []
                cells = []

                while node.parent:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent

                cells.append(node.state)
                
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
    world = VacuumWorldSolver('vacuum_world.csv')
    world.solve()
    world.print_solution()
