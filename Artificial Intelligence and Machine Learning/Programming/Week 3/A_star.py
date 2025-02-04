"""Generalised A* Search algorithm. AStarSearch"""

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
        return self.fscore < other.fscore
    
class AStarProblem:
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal

    def neighbours(self, state):
        """Returns list of neighbouring states. Should be implemented in subclass"""
        raise NotImplementedError
    
    def heuristic(self, state):
        """Returns heuristic value used in A* search method"""
        raise NotImplementedError

    def is_goal(self, state):
        return state == self.goal

    def astar(self):
        """Solves Problem using specific heuristic defined by subclass"""
        frontier: PriorityQueue[Node] = PriorityQueue()
        frontier.put(Node(self.start, 0, self.heuristic(self.start)))
        closed_set = set()

        while not frontier.empty():
            current = frontier.get()

            if self.is_goal(current.state):
                return self.reconstruct_path(current)
            
            closed_set.add(current.state)

            for neighbour, cost in self.neighbours(current.state):
                if neighbour in closed_set:
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
