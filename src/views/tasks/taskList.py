from textual.app import ComposeResult
from textual.containers import Container
from src.components.Lista.Lista import TablaCambios
from src.backend.controllers.taskController import TaskController
from src.components.Lista.Lista import UpdateTask
from src.views.tasks.tasksView import TaskView
from textual import on


class TaskList(Container):
    def __init__(self): 
        super().__init__() 
        self.tabla_tareas=TablaCambios("Tareas") 
        self.taskController = TaskController()
        self.formulario_edicion = None
        
    def compose(self)->ComposeResult: 
        yield self.tabla_tareas

    def _on_mount(self)-> None:
        self.cargar_tareas()

    def cargar_tareas(self):
        response = self.taskController.getTasks()

        if response["message"]=="Exito al Obtener las tareas":
           tareas= response["data"] 
           self.tabla_tareas.data(tareas)
        else:
            self.notify("Error: ",response["message"])

    def cargar_tareas_by_ID(self,id:int):
        response = self.taskController.getTasksById(id)

        if response["message"]=="Exito al Obtener la tarea":
           tarea= response["data"] 
           self.tabla_tareas.data(tarea)
        else:
            self.notify("Error: ",response["message"], severity="error")
    
    @on(UpdateTask)
    def on_update_task(self, event: UpdateTask):
        self.tabla_tareas.remove()
        self.formulario_edicion = TaskView(event.task_id, parent_list=self)
        self.mount(self.formulario_edicion)
    
    def mostrar_tabla(self):
        self.remove_children()
        self.tabla_tareas = TablaCambios("Tareas")
        self.mount(self.tabla_tareas)
        self.call_after_refresh(self.cargar_tareas)
