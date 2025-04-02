from rich.text import Text
from datetime import datetime
from src.components.Lista import estilo
from textual.widgets import DataTable, Static
from textual.app import ComposeResult, Widget
from textual.containers import VerticalScroll
from src.backend.controllers.eventController import EventController 
from src.backend.controllers.taskController import TaskController 
from textual.message import Message

class UpdateEvent(Message):
    def __init__(self, event_id: int) -> None:
        super().__init__()
        self.event_id = event_id

class UpdateTask(Message):
    def __init__(self, task_id: int) -> None:
        super().__init__()
        self.task_id = task_id

class TablaCambios(Widget):    
    def __init__(self, tipo: str):
        super().__init__()
        self.tipo = tipo
        self.table = DataTable()
        self.row_keys = []
        self.eventController = EventController() 
        self.taskController = TaskController()

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Static(f"GESTION DE {self.tipo.upper()}", classes="titulo")
            yield self.table
    
    def on_mount(self) -> None:
        self.theme = estilo.arctic_theme  
        self.theme = "Tabla"

        self.table = self.query_one(DataTable)
        self.table.zebra_stripes = 1
        self.table.header_height = 1

        if self.tipo.upper() == "EVENTOS":
            headers = ["N°","Título", "Descripción", "Ubicación", "Inicio", "Fin", "Actualizar", "Eliminar"]
        elif self.tipo.upper() == "TAREAS":
            headers = ["N°","Título", "Descripción", "Prioridad", "Vencimiento", "Actualizar", "Eliminar"]
        
        header_row = [Text(f" {col} \n  ", style="bold", justify="center") for col in headers]
        self.table.add_columns(*header_row)

    def data(self, casos) -> None:
        self.row_keys = []
        self.table.clear()
        self.num=1
        
        if self.tipo.upper() == "EVENTOS":
            sorted_rows = sorted(casos, key=lambda caso: datetime.strptime(caso[4], "%Y-%m-%d"))
            for caso in sorted_rows:
           
                descripcion_full=caso[2]
                descripcion = caso[2][:20] + "..." if len(caso[2]) > 25 else caso[2]
                
                inicio = datetime.strptime(caso[4], "%Y-%m-%d").strftime("%d-%m-%Y")
                fin = datetime.strptime(caso[5], "%Y-%m-%d").strftime("%d-%m-%Y")

                fila = [
                    Text(str(self.num), justify="center", style="italic"),
                    Text(caso[1], justify="left", style="italic"),
                     Text(descripcion, justify="left", style="italic"),
                    Text(caso[3], justify="left", style="italic"),
                    Text(inicio [:10], justify="center", style="italic"),
                    Text(fin [:10], justify="center", style="italic"),
                    Text("🔂"[:1], justify="center"),
                    Text("❌"[:1], justify="center"), 
                ]
                key = f"row-{str(caso[0])}"
                self.table.add_row(*fila, key=key)
                self.row_keys.append((key,descripcion_full,caso[0]))
                self.num+=1

        elif self.tipo.upper() == "TAREAS":
            sorted_rows = sorted(casos, key=lambda caso: datetime.strptime(caso[4], "%Y-%m-%d"))
            for caso in sorted_rows:
                descripcion_full=caso[2]
                descripcion = caso[2][:25] + "..." if len(caso[2]) > 25 else caso[2]
                vencimiento = datetime.strptime(caso[4], "%Y-%m-%d").strftime("%d-%m-%Y")
                fila = [
                    Text(str(self.num), justify="center", style="italic"),
                    Text(caso[1], justify="left", style="italic"),
                    Text(descripcion, justify="left", style="italic"),
                    Text(str(caso[3]), justify="left", style="italic"),
                    Text(vencimiento [:12], justify="center", style="italic"),
                    Text("🔂"[:1], justify="center"),
                    Text("❌"[:1], justify="center"), 
                ]
                key = f"row-{str(caso[0])}"
                self.table.add_row(*fila, key=key)
                self.row_keys.append((key,descripcion_full,caso[0]))
                self.num+=1


    def on_data_table_cell_selected(self, event: DataTable.CellSelected) -> None:
        row, col = event.coordinate
             
        key_to_remove, descripcion_full, id_caso = self.row_keys[row]

        if self.tipo.upper() == "EVENTOS":
            if col == 2:
                self.notify(f"Descripción: {descripcion_full}", severity="information")

            if col == 6:  
                evento_id = id_caso
                self.post_message(UpdateEvent(evento_id))

        if self.tipo.upper() == "EVENTOS":
            if col == 7:  
                evento_id = id_caso
                response = self.eventController.deleteEvent(evento_id)
                self.row_keys = [key for idx, key in enumerate(self.row_keys) if idx != row]
                self.table.remove_row(key_to_remove) 
                self.notify(f"✅ {response['message']}", severity="success")
                

        if self.tipo.upper() == "TAREAS":

            if col == 2:
                self.notify(f"Descripción: {descripcion_full}", severity="information")

            if col == 5: 
                tarea_id = id_caso
                self.post_message(UpdateTask(tarea_id))

            if col == 6:  
                task_id = id_caso
                response = self.taskController.deleteTask(task_id)
                self.row_keys = [key for idx, key in enumerate(self.row_keys) if idx != row]

                self.table.remove_row(key_to_remove)
                self.notify(f"✅ {response['message']}", severity="success")
