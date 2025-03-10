from textual.app import ComposeResult
from textual.containers import Container
from src.components.Lista.Lista_real import TablaCambios

class TaskList(Container):
    def compose (self) -> ComposeResult:
        yield TablaCambios("Tareas")