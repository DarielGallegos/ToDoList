
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label, Static, Markdown
from src.components.Lista.Lista_real import TablaCambios

class EventList(Container):
    def compose (self) -> ComposeResult:
        yield TablaCambios("Eventos")
