from enum import Enum
from common.direction import Direction
from robot.robot import Robot
from algorithm.node import *
from math import trunc, pi

import dearpygui.dearpygui as dpg

class Color(Enum):
    EMPTY       = [255, 255, 255]
    ROBOT       = [85, 168, 104]
    OBSTACLE    = [37, 37, 38]

class SimulationWindow():

    def __init__(self, window_tag):
        self.window_tag = window_tag
        self.window_size = dpg.get_item_height(window_tag) - 16
        self.side_cell_count = 20
        self.cell_size = self.window_size / self.side_cell_count

        # determine window boundaries
        self.min_x = 0
        self.min_y = 0
        self.max_x = self.window_size
        self.max_y = self.window_size

        self.ui_grid = {}

        self.obstacles = {}
        self.robot = Robot(self.side_cell_count, self.obstacles)

    def initialize_grid(self):

        if(len(self.obstacles) > 0):
            for o in self.obstacles:
                self.remove_obstacle((o.x, o.y))

        self.robot.direction = Direction.NORTH
        self.robot.x = 0
        self.robot.y = self.side_cell_count - 1

        self.drawlist = dpg.add_drawlist(parent=self.window_tag, width=self.window_size + 1, height=self.window_size + 1, show=True)
        span = 0

        # draw grid cells
        for row in range(self.side_cell_count):
            for col in range(self.side_cell_count):
                node = dpg.draw_rectangle(
                    [self.min_x + col * self.cell_size, self.min_y + row * self.cell_size], 
                    [self.min_x + (col + 1) * self.cell_size, (row + 1) * self.cell_size], 
                    parent=self.drawlist
                )

                self.ui_grid[(col, row)] = node
                span += self.cell_size
        
        # Draw lines between cells (grid)
        for col in range(len(self.ui_grid)):
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
            self.clickhandler = dpg.add_mouse_click_handler(callback=self.cell_clicked)

        dpg.configure_item("btn_up", callback=self.btn_up_clicked)
        dpg.configure_item("btn_down", callback=self.btn_down_clicked)
        dpg.configure_item("btn_left", callback=self.btn_left_clicked)
        dpg.configure_item("btn_right", callback=self.btn_right_clicked)

        self.update_drawlist()

    def btn_up_clicked(self):
        self.robot.move_up()
        self.update_drawlist()

    def btn_down_clicked(self):
        self.robot.move_down()
        self.update_drawlist()

    def btn_left_clicked(self):
        self.robot.move_left()
        self.update_drawlist()

    def btn_right_clicked(self):
        self.robot.move_right()
        self.update_drawlist()

    def cell_clicked(self):
        mouse_pos = dpg.get_mouse_pos()
        mouse_pos[1] -= 1  # account for window padding

        if (mouse_pos[1] > self.max_y or mouse_pos[1] < self.min_y or mouse_pos[0] < 0 or mouse_pos[0] > self.max_x or dpg.get_active_window() != self.window_tag):
            return

        mouse_pos = dpg.get_drawing_mouse_pos()

        within_x = mouse_pos[0] >= self.min_x and mouse_pos[0] <= self.max_x
        within_y = mouse_pos[1] >= self.min_y and mouse_pos[1] <= self.max_y

        pos = (trunc(mouse_pos[0]//self.cell_size), trunc(mouse_pos[1]//self.cell_size))
        is_clearing = True if (dpg.is_mouse_button_down(1)) else False  # True if right clicking

        if (within_x and within_y):

            robot_neighbours = self.robot.get_neighbours()

            if(is_clearing):
                if(pos not in robot_neighbours):
                    self.remove_obstacle(pos)
            else:
                if(pos not in robot_neighbours):
                    self.set_obstacle(pos)

            self.update_drawlist()

    def update_drawlist(self):
        for pos in self.ui_grid:
            cell = self.ui_grid[pos]
            node_color = None

            robot_neighbours = self.robot.get_neighbours()
            if(pos in self.obstacles):
                node = self.obstacles[pos]
                node_color = Color.OBSTACLE.value

                # apply transform (cause we only create the direction rect when obstacale is added)
                angle = pi * self.__to_angle(node.direction) / 180.0
                x_offset = 0
                y_offset = 0

                if(node.direction == Direction.NORTH):
                    x_offset = 0
                    y_offset = 0
                elif (node.direction == Direction.SOUTH):
                    x_offset = y_offset = self.cell_size
                    pass
                elif (node.direction == Direction.EAST):
                    y_offset = self.cell_size
                    x_offset = self.cell_size - 5
                    pass
                elif (node.direction == Direction.WEST):
                    x_offset = 5
                    pass

                translate = ((node.x * self.cell_size + x_offset), (node.y * self.cell_size + y_offset))
                dpg.apply_transform(str(node), dpg.create_translation_matrix(translate) * dpg.create_rotation_matrix(angle=angle, axis=[0, 0, -1]))
            elif(pos == self.robot.get_position() or pos in robot_neighbours):
                node_color = color=Color.ROBOT.value
            else:
                node_color = color=Color.EMPTY.value

            dpg.configure_item(cell, color=node_color, fill=node_color)

    def set_obstacle(self, pos):

        if(pos in self.obstacles):
            self.rotate_obstacle(pos)
            return

        if(self.robot.get_position() == pos):
            return
        else:

            if(len(self.obstacles) >= 5):
                return

            cell = self.ui_grid[pos]
            node =  Node(pos)
            self.obstacles[pos] = node

            with dpg.draw_node(tag=str(node), parent=self.drawlist):
                dpg.draw_rectangle(
                    [0, 0],
                    [self.cell_size, 5],
                    color=Color.ROBOT.value,
                    fill=Color.ROBOT.value,
                )

    def rotate_obstacle(self, pos):
        node = self.obstacles[pos]

        curr_idx = list(Direction).index(node.direction)
        next_idx = (curr_idx + 1) % len(Direction)
        node.direction = list(Direction)[next_idx]

    def remove_obstacle(self, pos):
        if(pos in self.obstacles):
            node = self.obstacles.pop(pos)
            dpg.delete_item(str(node))

    def __to_angle(self, direction):
        if direction == Direction.NORTH:
            return 0
        elif direction == Direction.EAST:
            return 90
        elif direction == Direction.SOUTH:
            return 180
        elif direction == Direction.WEST:
            return  270