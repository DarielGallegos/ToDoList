from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label, Static, Markdown
from src.components.FormEvent.FormEvent import FormularioEvento, FormularioEventoMensaje # type: ignore
from src.backend.controllers.eventController import EventController
from src.backend.models.data.events import Events 

class EventView(Container):
    def compose(self) -> ComposeResult:
        yield Label("REGISTRO DE EVENTO", classes="titulo")
        
        self.formulario = FormularioEvento([
            {"id": "titulo", "label": "Título", "tipo": "texto", "placeholder": "Escriba un título", "max_length": 50, "requerido": True},
            {"id": "descripcion", "label": "Descripción", "tipo": "textarea", "requerido": True},
            {"id": "ubicacion", "label": "Ubicación", "tipo": "texto", "placeholder": "Escriba la ubicación", "requerido": True}, 
        ])
        yield self.formulario
    
    def on_formulario_evento_mensaje(self, message: FormularioEventoMensaje):

        datos = message.datos
        event_controller = EventController()

        evento = Events(
            titulo=datos["titulo"],
            descripcion=datos["descripcion"],
            ubicacion=datos["ubicacion"],
            fecha_inicio=datos["fecha_inicio"],
            fecha_final=datos["fecha_final"]
        )

        try:
            response = event_controller.createEvent(evento)

            self.notify(response["message"], 
                        severity="success" if response["status"] else "error")

        except Exception as e:
            self.notify(str(e), severity="error")