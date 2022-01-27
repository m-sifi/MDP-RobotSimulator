from common.direction import Direction

class Robot():

    def __init__(self, grid_size, obstacles):
        self.ROBOT_SIZE = 3
        self.GRID_SIZE = grid_size
        self.obstacles = obstacles

        self.x = self.y = 0
        self.direction = Direction.NORTH
        pass

    def get_position(self):
        return (self.x, self.y)

    def move(self, new_pos):
        old_pos = self.x, self.y
        self.x, self.y = new_pos

        if(self.is_within_grid() == False or self.is_in_obstacle()):
            self.x, self.y = old_pos

    def move_up(self):
        dest = (self.x, self.y - 1)
        self.move(dest)

    def move_down(self):
        dest = (self.x, self.y + 1)
        self.move(dest)

    def move_left(self):
        dest = (self.x - 1, self.y )
        self.move(dest)

    def move_right(self):
        dest = (self.x + 1, self.y)
        self.move(dest)

    def get_neighbours(self):
        neighbours = []

        for i in range(self.ROBOT_SIZE):
            for j in range(self.ROBOT_SIZE):
                pos = (self.x + i, self.y - j)
                neighbours.append(pos)

        return neighbours

    def is_in_obstacle(self):
        neighbours = self.get_neighbours()

        for pos in neighbours:
            for node in self.obstacles:
                print(f"{pos} == {node}")
                if(pos == node):
                    return True

        return False
            

    def is_within_grid(self):
        neighbours = self.get_neighbours()

        for pos in neighbours:
            x, y = pos
            if(((0 <= x <= self.GRID_SIZE - 1) and (0 <= y <= self.GRID_SIZE - 1)) == False):
                return False
        
        return True
    
