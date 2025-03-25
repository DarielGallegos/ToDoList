from textual.app import ComposeResult
<<<<<<< Updated upstream
from textual.containers import Container
from textual.widgets import Label
class TaskList(Container):

    def compose(self) -> ComposeResult:
        yield Container(Label("Contenido de Carga nuevo de List"))
=======
from textual.containers import Container,Label
from src.components.Lista.Lista_real import TablaCambios
from src.backend.controllers.taskController import TaskController


class TaskList(Container):
    def compose (self) -> ComposeResult:         
        yield Label("Lista de Tareas")
        self.tabla_tareas=TablaCambios("Tareas")
        yield self.tabla_tareas

    def _on_mount(self)-> None:
        self.taskController = TaskController()
        
        self.Cargar_tarea()

    def cargar_eventos(self):
        response = self.taskController().getTask()

        if response["message"]=="Exito al Obtener las Tareas":
           tareas= response["data"] 
        
        self.tabla_eventos.table.clear()
        for tarea in tareas:
            fila= [
                tarea["id"],
                tarea["titulo"],
                tarea["descripción"],
                tarea["fecha_inicio"],
                tarea["fecha_final"],
                "🔂", 
                "❌"   
            ]
            self.tabla_tareas.table.add_row(*fila)
        else:
            print("Error: ",response["message"])

    def cargar_eventos_by_id(self, id: int):
        response= self.eventController.getTaskById(id)

        if response["message"]== "Exito al Obtener la tarea":
            tarea = response["data"]

            self.tabla_tareas.table.clear()
            fila=[
                tarea["id"],
                tarea["titulo"],
                tarea["descripción"],
                tarea["fecha_inicio"],
                tarea["fecha_final"],
                "🔂",  
                "❌"   
            ]
            self.tabla_tareas.tabla.add_row(*fila)
        else:
            print("Error: ",response["message"])
>>>>>>> Stashed changes

