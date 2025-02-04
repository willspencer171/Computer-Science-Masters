"""Generalised A* Search algorithm. AStarProblem acts as an abstract class since the
neighbours and heuristic functions are not implemented. This just requires that
any subclass of the AStarProblem has a heuristic function and a way to generate
neighbours"""

from queue import PriorityQueue
from typing import Self

class Node:
    def __init__(self, state, gscore, hscore, parent: Self=None):
        self.state = state

        self.gscore = gscore
        self.hscore = hscore
        self.fscore = gscore + hscore

        self.parent = parent

    def __lt__(self, other: Self):
        """Needed for heap data structure in PriorityQueue"""
        return self.fscore < other.fscore
    
class AStarProblem:
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal

    def neighbours(self, state):
        """Returns list of neighbouring states. Should be implemented in subclass"""
        raise NotImplementedError
    
    def heuristic(self, state):
        """Returns heuristic value used in A* search method. Should be implemented in subclass"""
        raise NotImplementedError

    def is_goal(self, state):
        return state == self.goal

    def astar(self) -> tuple[list[Node], int] | None:
        """Solves Problem using specific heuristic defined by subclass
        ---
        
        Returns
        ---
        tuple containing the solution path and number of expanded nodes or None if no solution found"""
        frontier: PriorityQueue[Node] = PriorityQueue()     # Type hints, helpful for when coding implementations
        frontier.put(Node(self.start, 0, self.heuristic(self.start)))   # Initialise first node
        closed_set = set()      # Graph form of problem

        while not frontier.empty():     # If the frontier is empty, there is no solution
            current = frontier.get()

            if self.is_goal(current.state):     # Goal condition
                print(f"Goal Found at the {len(closed_set)}th state")
                return (self.reconstruct_path(current), len(closed_set))
            
            closed_set.add(current.state)

            for neighbour, cost in self.neighbours(current.state):
                if neighbour in closed_set: # skip duplicates
                    continue

                g_cost = current.gscore + cost
                h_cost = self.heuristic(current.state)
                neighbour_node = Node(neighbour, g_cost, h_cost, current)

                for open_node in frontier.queue:
                    if open_node.state == neighbour and open_node.fscore <= neighbour_node.fscore:
                        break
                else:
                    frontier.put(neighbour_node)
                
        return None
    
    def reconstruct_path(self, node: Node):
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]
    
    def ida_star(self):
        """Main IDA* search"""
        bound = self.heuristic(self.start)
        path = [self.start]

        while True:
            t = self._search(path, 0, bound)
            if t == "FOUND":
                return path
            if t == float("inf"):
                return None  # No solution
            bound = t  # Increase cost limit

    def _search(self, path, g, bound):
        """Recursive depth-limited DFS"""
        state = path[-1]
        h = self.heuristic(state)
        f = g + h
        if f > 45:
            print(f)
        if f > bound:
            return f
        if state == self.goal:
            return "FOUND"

        min_cost = float("inf")
        for neighbour, _ in self.neighbours(state):
            if neighbour in path:  # Avoid cycles
                continue
            path.append(neighbour)
            t = self._search(path, g + 1, bound)
            if t == "FOUND":
                return "FOUND"
            if t < min_cost:
                min_cost = t
            path.pop()
        
        return min_cost
