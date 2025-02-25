from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label
class TaskView(Container):

    def compose(self) -> ComposeResult:
        yield Container(Label("Contenido de Carga nuevo"), id="taskView")

