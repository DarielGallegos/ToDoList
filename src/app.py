from src.views.main import Views
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer
class ToDoList(App):
 ## Define la ruta del archivo CSS
 CSS_PATH = "./css/main.tcss"

 ## Define BINDINGS
 BINDINGS = [
  Binding("ctrl+x", "quit", "Salir"),
 ] 
 def compose(self) -> ComposeResult:
  ## Asigna el titulo al aplicativo
  self.screen.title = "To Do List"
  yield Header()
  yield Views(id="main")
  yield Footer()