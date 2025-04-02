from textual.app import ComposeResult
from textual.containers import Container 
from src.components.Lista.Lista import TablaCambios 
from src.backend.controllers.eventController import EventController 
from src.views.events.eventView import EventView
from textual import on
from src.components.Lista.Lista import UpdateEvent
from src.views.events.eventView import EventView 

class EventList(Container): 
    def __init__(self): 
        super().__init__() 
        self.tabla_eventos=TablaCambios("Eventos") 
        self.eventController = EventController()
        self.formulario_edicion = None 
        
    def compose(self)->ComposeResult: 
        yield self.tabla_eventos 
    
    def _on_mount(self)-> None: 
        self.cargar_eventos() 
    
    def cargar_eventos(self): 
        try:
            response = self.eventController.getEvents() 
            
            if response["message"]=="Exito al Obtener los eventos": 
                eventos= response["data"] 
                self.tabla_eventos.data(eventos)
        except Exception as e:
              self.notify(str(e), severity="error")
        
    def cargar_evento_by_ID(self,id:int):
        try:
            response = self.eventController.getEventById(id)

            if response["message"]=="Exito al Obtener los eventos":
                evento= response["data"] 
                self.tabla_eventos.data(evento)
        except Exception as e:
              self.notify(str(e), severity="error")

    @on(UpdateEvent)
    def on_update_event(self, event: UpdateEvent):
        """Muestra el formulario de edición"""
        self.tabla_eventos.remove()
        self.formulario_edicion = EventView(event.event_id, parent_list=self) 
        self.mount(self.formulario_edicion)

    def mostrar_tabla(self):
        self.remove_children()
        self.tabla_eventos = TablaCambios("Eventos")
        self.mount(self.tabla_eventos)
        self.call_after_refresh(self.cargar_eventos)
