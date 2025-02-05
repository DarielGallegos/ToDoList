import curses
from curses import window
from src.components.submenu.submenu import SubMenu

options = ["Eventos", "Tareas", "Salir"]

class Menu:
    def __init__(self, stdscr : window):
        self.stdscr = stdscr
        self.selected_row = 0

    def display_menu(self):
        self.__print_menu()
        submenu = SubMenu(self.stdscr, self.selected_row)
        while 1:
            key = self.stdscr.getch()
            self.stdscr.clear()
            if key == curses.KEY_UP and self.selected_row > 0:
                self.selected_row -= 1
            elif key == curses.KEY_DOWN and self.selected_row < len(options)-1:
                self.selected_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if self.selected_row != 2:
                    submenu.display_submenu()
                else:
                    break
            
            self.__print_menu()
            self.stdscr.refresh()
   
    def __print_menu(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        for idx, row in enumerate(options):
            x = w//2 - len(row)//2
            y = h//2 - len(options)//2 + idx
            if idx == self.selected_row:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, row)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, row)
        self.stdscr.refresh()