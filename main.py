import dearpygui.dearpygui as dpg
from ui.RobotPath import RobotPath

def main():
    dpg.create_context()
    
    app = RobotPath()
    app.configure_viewport()

    dpg.start_dearpygui()

if __name__ == "__main__":
    main()