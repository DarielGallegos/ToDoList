from textual.app import ComposeResult
from textual.widgets import Label, Static
from textual.containers import Container

class Default_view(Container):
    def compose(self) -> ComposeResult:
         yield Label("░▀█▀░█▀█░█▀▀░█░█░▀█▀░█░█░▀█▀ \n"
                     "░░█░░█▀█░▀▀█░█▀▄░░█░░█░█░░█░ \n"
                     "░░▀░░▀░▀░▀▀▀░▀░▀░░▀░░▀▀▀░▀▀▀ \n", classes="name")
    