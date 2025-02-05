import curses
from curses import window
from src.components.menu.menu import Menu
def main(stdscr : window):
    try:
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        stdscr.clear()
        menu = Menu(stdscr = stdscr)
        menu.display_menu()
    except KeyboardInterrupt:
        print("\nMonitoreo finalizado")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
 