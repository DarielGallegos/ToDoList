from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label, Static, Markdown
from src.components.FormEvent.FormEvent import FormularioEvento, FormularioEventoMensaje # type: ignore

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
        self.notify(
            f"Evento creado:\n"
            f"Título: {message.datos['titulo']}\n"
            f"Descripcion: {message.datos['descripcion']}\n"
            f"Ubicacion: {message.datos['ubicacion']}\n"
            f"Fecha Inicio: {message.datos['fecha_inicio']}\n"
            f"Fecha Final: {message.datos['fecha_final']}\n",
            severity="success"
        )

