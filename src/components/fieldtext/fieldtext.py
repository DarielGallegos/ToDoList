from curses import window, newwin
from curses.textpad import Textbox, rectangle

class FieldText:
    def __init__(self, stdscr : window, y:int, x:int, width:int, height:int, label:str):
        self.stdscr = stdscr
        self.y = y
        self.x = x
        self.width = width
        self.height = height
        self.label = label

    def draw(self):
        self.stdscr.addstr(self.y, self.x, self.label)
        #editwin = newwin(self.height, self.width, self.y, self.x)
        #rectangle(self.stdscr, self.y-1, self.x-1, self.y+self.height, self.x+self.width)
        #editwin.refresh()
        #box = Textbox(editwin)
        #box.edit()

