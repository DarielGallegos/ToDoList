import curses
from curses import window
from src.views.tasks.tasksView import TaskView

sub_menu = ["Listar", "Crear", "Actualizar", "Eliminar", "Volver"]

class SubMenu:
    def __init__(self, stdscr:window, selected_opt, selected_row = 0):
        self.stdscr = stdscr
        self.selected_opt = selected_opt
        self.selected_row = selected_row

    def display_submenu(self):
        self.__print_submenu()
        while 1:
            key = self.stdscr.getch()
            self.stdscr.clear()
            if key == curses.KEY_UP and self.selected_row > 0:
                self.selected_row -= 1
            elif key == curses.KEY_DOWN and self.selected_row < len(sub_menu)-1:
                self.selected_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if self.selected_row != 4:
                    self.__menu_selector()

            self.__print_submenu()
            self.stdscr.refresh()
    
    def __print_submenu(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        for idx, row in enumerate(sub_menu):
            x = w//2 - len(row)//2
            y = h//2 - len(sub_menu)//2 + idx
            if idx == self.selected_row:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, row)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, row)
        self.stdscr.refresh()

    def __menu_selector(self):
        if self.selected_row == 1:
            view = TaskView(stdscr=self.stdscr, title="Crear Tarea")
            view.show()
        elif self.selected_row == 2:
            view = TaskView(stdscr=self.stdscr, title="Actualizar Tarea")
            view.show()
        elif self.selected_row == 3:
            view = TaskView(stdscr=self.stdscr, title="Eliminar Tarea")
            view.show()
        elif self.selected_row == 0:
            view = TaskView(stdscr=self.stdscr, title="Listar Tareas")
            view.show()
        self.stdscr.clear()
        self.stdscr.refresh()