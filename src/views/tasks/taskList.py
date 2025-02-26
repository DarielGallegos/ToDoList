from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label
class TaskList(Container):

    def compose(self) -> ComposeResult:
        yield Container(Label("Contenido de Carga nuevo de List"))

