from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label, Static, Markdown
from src.components.fieldtext.fieldtext import FormularioInput, FormularioMensaje
from src.backend.controllers.taskController import TaskController
from src.backend.models.data.task import Tareas

class TaskView(Container):
    def compose(self) -> ComposeResult:
        yield Label("REGISTRO DE TAREAS", classes="titulo")
        
        self.formulario = FormularioInput([
            {"id": "titulo", "label": "Título", "tipo": "texto", "placeholder": "Escriba un título", "max_length": 50, "requerido": True},
            {"id": "descripcion", "label": "Descripción", "tipo": "textarea", "requerido": True},
        ])
        yield self.formulario
    
    def on_formulario_mensaje(self, message: FormularioMensaje):

        datos = message.datos
        task_controller = TaskController()

        tarea = Tareas(
            titulo=datos["titulo"],
            descripcion=datos["descripcion"],
            prioridad =datos["prioridad"],
            fecha_vencimiento=datos["fecha_vencimiento"]
        )

        try:
            response = task_controller.createTask(tarea)

            self.notify(response["message"], 
                        severity="success" if response["status"] else "error")

        except Exception as e:
            self.notify(str(e), severity="error")
