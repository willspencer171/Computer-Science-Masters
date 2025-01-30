import sys
from typing import Self, Type

class State:
    pass

class Action:
    pass

class Node:
    def __init__(self, state: State, parent: Self, action: Action):
        self.state = state
        self.parent = parent
        self.action = action

class Problem:
    def __init__(self, state_cls: Type[State], action_cls: Type[Action]):
        pass

class Frontier:
    def __init__(self):
        self.frontier = []

    def add(self, node: Node):
        self.frontier.append(node)
    
    def contains_state(self, state: State):
        return any(node.state == state for node in self.frontier)
    
    @property
    def is_empty(self):
        return len(self.frontier) == 0
    
class QueueFrontier(Frontier):
    def __init__(self):
        super().__init__()

    def pop(self):
        return self.frontier.pop(0)

class StackFrontier(Frontier):
    def __init__(self):
        super().__init__()
    
    def pop(self):
        return self.frontier.pop()
