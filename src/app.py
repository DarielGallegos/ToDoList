from src.views.main import Views
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
class ToDoList(App):
	## Define la ruta del archivo CSS
	CSS_PATH = "./css/main.tcss"

	def compose(self) -> ComposeResult:
		## Asigna el titulo al aplicativo
		self.screen.title = "TaskTUI"
		yield Header()
		yield Views(id="main")
		yield Footer()