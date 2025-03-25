from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label, Static, Markdown
from src.components.Lista.Lista_real import TablaCambios
from src.backend.controllers.eventController import EventController

class EventList(Container):
    def compose (self) -> ComposeResult:
        yield Label("Lista de Eventos")
        self.tabla_eventos = TablaCambios("Eventos")
        yield self.tabla_eventos


    def _on_mount(self)-> None:
        self.eventController = EventController()
        
        self.Cargar_eventos()

    def cargar_eventos(self):
        response = self.eventController.getEvents()

        if response["message"]=="Exito al Obtener los eventos":
           eventos= response["data"] 
        
        self.tabla_eventos.table.clear()
        for evento in eventos:
            fila= [
                evento["id"],
                evento["titulo"],
                evento["descripción"],
                evento["fecha_inicio"],
                evento["fecha_final"],
                "🔂", 
                "❌"   
            ]
            self.tabla_eventos.table.add_row(*fila)
        else:
            print("Error: ",response["message"])

    def cargar_eventos_by_id(self, id: int):
        response= self.eventController.getEventById(id)

        if response["message"]== "Exito al Obtener los eventos":
            evento = response["data"]

            self.tabla_eventos.table.clear()
            fila=[
                evento["id"],
                evento["titulo"],
                evento["descripción"],
                evento["fecha_inicio"],
                evento["fecha_final"],
                "🔂",  
                "❌"   
            ]
            self.tabla_eventos.tabla.add_row(*fila)
        else:
            print("Error: ",response["message"])

