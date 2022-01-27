from common.direction import Direction
from enum import Enum
from math import pi

class Node():
    def __init__(self, pos):
        self.x, self.y = pos
        self.direction = Direction.NORTH

    def __str__(self):
        return f"Node({self.x}, {self.y})"

class NodeState(Enum):
    EMPTY = 1
    START = 2
    OBSTACLE = 3
    PADDING = 4