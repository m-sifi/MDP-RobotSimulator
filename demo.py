import dearpygui.dearpygui as dpg
from dearpygui.demo import show_demo

def main():
    dpg.create_context()
    dpg.create_viewport()
    dpg.setup_dearpygui()

    show_demo()

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()