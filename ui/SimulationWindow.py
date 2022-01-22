from algorithm.Node import Node, NodeState
import dearpygui.dearpygui as dpg
from math import trunc

class SimulationWindow():

    def __init__(self, window_tag):
        self.window_tag = window_tag
        self.window_size = dpg.get_item_height(window_tag) - 16
        self.side_cell_count = 20
        self.cell_size = self.window_size / self.side_cell_count

        self.colors = {
            NodeState.EMPTY: [255, 255, 255],
            NodeState.START: [85, 168, 104],
            NodeState.OBSTACLE: [37, 37, 38],
            NodeState.PADDING: [204, 185, 116],
        }

        # determine window boundaries
        self.min_x = 0
        self.min_y = 0
        self.max_x = self.window_size
        self.max_y = self.window_size

        self.grid = None
        self.node_grid = {}

    def initialize_grid(self):
        self.drawlist = dpg.add_drawlist(parent=self.window_tag, width=self.window_size + 1, height=self.window_size + 1, show=True)
        self.grid = []
        span = 0

        for y in range(self.side_cell_count):
            self.grid.append([])

            for x in range(self.side_cell_count):
                node = Node((x, y))
                self.grid[y].append(node)

        # Set start nodes
        start_node = self.grid[self.side_cell_count - 2][1]
        self.update_node_neighbours(start_node)

        start_node.state = NodeState.START

        for neighbour in start_node.neighbours:
            neighbour.state = NodeState.START

        # Draw grid
        for row in self.grid:
            for node in row:
                nodeident = dpg.draw_rectangle(
                    [self.min_x + node.x * self.cell_size, self.min_y + node.y * self.cell_size], 
                    [self.min_x + (node.x + 1) * self.cell_size, (node.y+ 1) * self.cell_size], 
                    color=self.colors[node.state], 
                    fill=self.colors[node.state], 
                    parent=self.drawlist
                )
                self.node_grid[(node.x, node.y)] = nodeident
                span += self.cell_size
        
        # Draw lines between cells (grid)
        for col in range(len(self.grid)):
            dpg.draw_rectangle(
                [self.min_x + col * self.cell_size, 0], 
                [self.min_x + (col + 1) * self.cell_size, span], 
                color=[0, 0, 0, 255], 
                fill=[0, 0, 0, 0], 
                thickness=2, 
                parent=self.drawlist
            )
            
            dpg.draw_rectangle(
                [0, self.min_y+col*self.cell_size],
                [span, self.min_y + (col + 1) * self.cell_size], 
                color=[0, 0, 0, 255], 
                thickness=2, 
                fill=[0, 0, 0, 0], 
                parent=self.drawlist
            )
        
        # Draw grid edges
        dpg.draw_line([0, 0], [0, self.window_size], color=[0, 0, 0], thickness=4, parent=self.drawlist)
        dpg.draw_line([0, 0], [self.window_size, 0], color=[0, 0, 0], thickness=4, parent=self.drawlist)
        dpg.draw_line([self.window_size, self.window_size], [0, self.window_size], color=[0, 0, 0], thickness=4, parent=self.drawlist)
        dpg.draw_line([self.window_size, self.window_size], [self.window_size, 0], color=[0, 0, 0], thickness=4, parent=self.drawlist)  
        
        # Add Mouse Event
        with dpg.handler_registry() as self.clickregistry:
            self.clickhandler = dpg.add_mouse_click_handler(
                callback=self.cell_clicked)

    def cell_clicked(self):
        genpos = dpg.get_mouse_pos()
        genpos[1] -= 1  # account for window padding

        if (genpos[1] > self.max_y or genpos[1] < self.min_y or genpos[0] < 0 or genpos[0] > self.max_x or dpg.get_active_window() != self.window_tag):
            return

        pos = dpg.get_drawing_mouse_pos()

        within_x = pos[0] >= self.min_x and pos[0] <= self.max_x
        within_y = pos[1] >= self.min_y and pos[1] <= self.max_y

        x_cell = trunc(pos[0]//self.cell_size)
        y_cell = trunc(pos[1]//self.cell_size)

        print(f"Clicked on ({x_cell}, {y_cell})")
        clearing = True if (dpg.is_mouse_button_down(1)) else False  # True if right clicking

        if (within_x and within_y):
            node = self.grid[y_cell][x_cell]
            self.update_node_neighbours(node)

            if type(node) == None:
                return

            tempstate = node.state
            if clearing:
                if (tempstate == NodeState.OBSTACLE):
                    for neighbour in node.neighbours:
                        neighbour.state = NodeState.EMPTY
                    
                    node.state = NodeState.EMPTY
            else:
                if (tempstate == NodeState.EMPTY):
                    for neighbour in node.neighbours:
                        neighbour.state = NodeState.PADDING
                    node.state = NodeState.OBSTACLE

            for neighbour in node.neighbours:
                self.draw_node(neighbour)
            self.draw_node(node)

    def node_from_pos(self, pos):
        y = pos[1]
        x = pos[0]

        if 0 <= x < self.side_cell_count and 0 <= y < self.side_cell_count:
            return self.grid[y][x]
        else:
            return None

    def update_node_neighbours(self, node):
        right = self.node_from_pos((node.x + 1, node.y))
        left = self.node_from_pos((node.x - 1, node.y))
        up = self.node_from_pos((node.x, node.y + 1))
        up_left = self.node_from_pos((node.x - 1, node.y + 1))
        up_right = self.node_from_pos((node.x + 1, node.y + 1))
        down = self.node_from_pos((node.x, node.y - 1))
        down_left = self.node_from_pos((node.x - 1, node.y - 1))
        down_right = self.node_from_pos((node.x + 1, node.y - 1))

        if right is not None and node.state is not NodeState.OBSTACLE:
            node.neighbours.append(right)
        if left is not None and node.state is not NodeState.OBSTACLE:
            node.neighbours.append(left)
        if up is not None and node.state is not NodeState.OBSTACLE:
            node.neighbours.append(up)
        if up_left is not None and node.state is not NodeState.OBSTACLE:
            node.neighbours.append(up_left)
        if up_right is not None and node.state is not NodeState.OBSTACLE:
            node.neighbours.append(up_right)
        if down is not None and node.state is not NodeState.OBSTACLE:
            node.neighbours.append(down)
        if down_left is not None and node.state is not NodeState.OBSTACLE:
            node.neighbours.append(down_left)
        if down_right is not None and node.state is not NodeState.OBSTACLE:
            node.neighbours.append(down_right)

    def draw_node(self, node):
        nodeident = self.node_grid[(node.x, node.y)]
        dpg.configure_item(nodeident, fill=self.colors[node.state])