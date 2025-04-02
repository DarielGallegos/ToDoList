from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label, Button
from src.components.fieldtext.fieldtext import FormularioInput, FormularioMensaje
from src.backend.controllers.taskController import TaskController
from src.backend.models.data.task import Tareas
from textual import events

class TaskView(Container):
    def __init__(self, tarea_id: int = None, parent_list=None):
        super().__init__()
        self.tarea_id = tarea_id 
        self.parent_list = parent_list
        self.task_controller = TaskController()
        self.formulario = None
        self.modo = "edicion" if tarea_id else "creacion" 

    def compose(self) -> ComposeResult:
        titulo = "EDITAR TAREA" if self.modo == "edicion" else "REGISTRAR TAREA"
        yield Label(titulo, classes="titulo")
        
        self.formulario = FormularioInput([
            {"id": "titulo", "label": "Título", "tipo": "texto", "placeholder": "Escriba un título", "max_length": 50, "requerido": True},
            {"id": "descripcion", "label": "Descripción", "tipo": "textarea", "requerido": True},
        ])
        yield self.formulario
    
    def on_mount(self):
        self.capture_key_events = True
        if self.modo == "edicion" and self.tarea_id:
            self.cargar_datos_tarea(self.tarea_id)
    
    def volver_a_lista(self):
        if self.parent_list:
            self.parent_list.mostrar_tabla()
            self.remove() 
        else:
            from src.views.tasks.taskList import TaskList
            container = self.app.query_one("#viewContainer") 
            container.remove_children()
            container.mount(TaskList())
        
        self.app.set_focus(None) 
        if self.parent_list:
            self.call_after_refresh(self.parent_list.tabla_tareas.focus)

    def guardar_evento(self):
        self.formulario.enviar_datos() 

    def cargar_datos_tarea(self, tarea_id: int):
        try:
            response = self.task_controller.getTaskById(tarea_id)
            if response["message"] == "Exito al Obtener la tarea" and isinstance(response["data"], (tuple, list)):
                tarea = response["data"]
                if len(tarea) >= 5:  
                    self.formulario.inputs["titulo"].value = str(tarea[1])
                    self.formulario.inputs["descripcion"].text = str(tarea[2])
                    
                    if hasattr(self.formulario, 'select_prioridad'):
                        self.formulario.select_prioridad.value = str(tarea[3])
                    
                    if hasattr(self.formulario, 'calendario_vencimiento'):
                        fecha = tarea[4].strftime("%Y-%m-%d") if hasattr(tarea[4], 'strftime') else str(tarea[4])
                        self.formulario.calendario_vencimiento.selected_date = fecha
                        
        except Exception as e:
            self.notify(f"Error al cargar datos: {str(e)}", severity="error")

    def on_formulario_mensaje(self, message: FormularioMensaje):
        try:
            tarea = Tareas(
                id=self.tarea_id if self.modo == "edicion" else None,
                titulo=message.datos["titulo"],
                descripcion=message.datos["descripcion"],
                prioridad=message.datos.get("prioridad", ""),
                fecha_vencimiento=message.datos.get("fecha_vencimiento", "")
            )

            if self.modo == "edicion":
                self.task_controller.updateTask(tarea)
            else:
                self.task_controller.createTask(tarea)
      
            if self.parent_list:
                self.parent_list.mostrar_tabla()
            else:
                self.volver_a_lista()
            
        except Exception as e:
            self.notify(f"Error al guardar: {str(e)}", severity="error")

    def on_key(self, event: events.Key) -> None:
        if event.key == "ctrl+b":
            self.volver_a_lista()