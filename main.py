import dearpygui.dearpygui as dpg
from ui.application import PathSimulatorApplication

def main():
    dpg.create_context()
    
    app = PathSimulatorApplication()
    app.configure_viewport()

    dpg.start_dearpygui()

if __name__ == "__main__":
    main()