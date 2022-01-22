from enum import Enum

class Node():
    def __init__(self, pos):
        self.x, self.y = pos
        self.state = NodeState.EMPTY
        self.neighbours = []

    def __str__(self):
        return f"Node({self.x}, {self.y}) state: {self.state}"

class NodeState(Enum):
    EMPTY = 1
    START = 2
    OBSTACLE = 3
    PADDING = 4