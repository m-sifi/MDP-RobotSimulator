import dearpygui.dearpygui as dpg
from ui.SimulationWindow import SimulationWindow

class RobotPath():
    def __init__(self):
        self.WINDOW_WIDTH = 1360
        self.WINDOW_HEIGHT = 900
        self.WINDOW_RESIZABLE = False

        self.PATH_WINDOW_SIZE = 880

        self.pathing = None

        self.main_window = None
        self.controls_window = None
        self.simulation_window = None

        self.__init_window()

    def configure_viewport(self):
        dpg.create_viewport()
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_viewport_title("Robot Path Simulation")
        dpg.set_viewport_resizable(self.WINDOW_RESIZABLE)
        dpg.set_viewport_width(self.WINDOW_WIDTH)
        dpg.set_viewport_height(self.WINDOW_HEIGHT)

    def __init_window(self):
        with dpg.window(label="RobotPath") as self.main_window:
            with dpg.child_window(label="Simulation", height=self.PATH_WINDOW_SIZE, width=self.PATH_WINDOW_SIZE, no_scrollbar=True, pos=[10, 10]) as self.simulation_window:
                pass

            with dpg.child_window(label="Controls_Info", width=450, pos=[self.PATH_WINDOW_SIZE + 20, 10], border=False, no_scrollbar=True) as self.controls_window:
                with dpg.collapsing_header(label="Controls", default_open=True) as controls_panel:
                    pass

        self.pathing = SimulationWindow(window_tag=self.simulation_window)
        self.pathing.initialize_grid()

        dpg.set_primary_window(self.main_window, True)