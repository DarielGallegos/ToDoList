from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label, Static, Markdown
from src.components.fieldtext.fieldtext import FormularioInput, FormularioMensaje

class TaskView(Container):
    def compose(self) -> ComposeResult:
        yield Label("REGISTRO DE TAREAS", classes="titulo")
        
        self.formulario = FormularioInput([
            {"id": "titulo", "label": "Título", "tipo": "texto", "placeholder": "Escriba un título", "max_length": 50, "requerido": True},
            {"id": "descripcion", "label": "Descripción", "tipo": "textarea", "requerido": True},
        ])
        yield self.formulario
    
    def on_formulario_mensaje(self, message: FormularioMensaje):
        self.notify(
            f"Tarea creada:\n"
            f"Título: {message.datos['titulo']}\n"
            f"Descripción: {message.datos['descripcion']}\n"
            f"Prioridad: {message.datos['prioridad']}\n"
            f"Fecha de Vencimiento: {message.datos['fecha_vencimiento']}",
            severity="success"
        )
