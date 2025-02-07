from curses import window
class MainView:
    def __init__(self, stdscr:window, title:str):
        self.stdscr = stdscr
        self.title = title

    