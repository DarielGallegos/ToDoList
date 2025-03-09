from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label
from src.components.fieldtext.fieldtext import MensajeAccion, NombreInput

class EventView(Container):
    
    def compose(self) -> ComposeResult:

        yield Container(FormularioInput())
        
        yield Container(Label("Eventos", classes="title"))
        yield Container(NombreInput())

    def on_formulario_mensaje(self, message: MensajeAccion):
        
        self.notify(
            f"Acción realizada: {message.accion}\n"
            f"Nombre: {message.titulo}",  
            severity="success" if message.accion == "Guardar" else 
                      "info" if message.accion == "Editar" else 
                      "warning"
        )
