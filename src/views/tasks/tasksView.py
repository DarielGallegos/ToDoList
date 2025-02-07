import curses
from curses import window
from src.views.main import MainView
from src.components.fieldtext.fieldtext import FieldText
class TaskView(MainView):
    def __init__(self, stdscr:window, title:str):
        super().__init__(stdscr, title)

    def show(self):
        self.__display_view()
        while 1:
            key = self.stdscr.getch()
            self.stdscr.clear()
            if key == curses.KEY_ENTER or key in [10, 13]:
                print("Hace algo")
                
            self.__display_view()
            self.stdscr.refresh()
    
    def __display_view(self):
        self.stdscr.clear()
        self.stdscr.addstr(0,0, self.title)
        text1 = FieldText(self.stdscr, 5, 10, 20, 5, "Nombre")
        text1.draw()
        self.stdscr.refresh()

