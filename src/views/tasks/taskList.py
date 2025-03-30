from textual.app import ComposeResult
from textual.containers import Container
from src.components.Lista.Lista import TablaCambios
from src.backend.controllers.taskController import TaskController


class TaskList(Container):
    def __init__(self): 
        super().__init__() 
        self.tabla_tareas=TablaCambios("Tareas") 
        self.taskController = TaskController() 
        
    def compose(self)->ComposeResult: 
        yield self.tabla_tareas

    def _on_mount(self)-> None:
        self.cargar_tareas()

    def cargar_tareas(self):
        try:
            response = self.taskController.getTasks()

            if response["message"]=="Exito al Obtener las tareas":
                tareas= response["data"] 
                self.tabla_tareas.data(tareas)
        except Exception as e:
              self.notify(str(e), severity="error")

    def cargar_tareas_by_ID(self,id:int):
        try: 
            response = self.taskController.getTasksById(id)

            if response["message"]=="Exito al Obtener la tarea":
                tarea= response["data"] 
                self.tabla_tareas.data(tarea)
        except Exception as e:
              self.notify(str(e), severity="error")