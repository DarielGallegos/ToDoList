from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label
from src.components.fieldtext.fieldtext import FormularioInput, FormularioMensaje

class EventView(Container):
    
    def compose(self) -> ComposeResult:

        yield Container(FormularioInput())

    def on_formulario_mensaje(self, message: FormularioMensaje):
        
        self.notify(
            f"Evento creado:\n"
            f"Título: {message.titulo}\n"
            f"Descripción: {message.descripcion}\n"
            f"Fecha: {message.fecha}",
            severity="success"
        )