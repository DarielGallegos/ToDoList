from textual.app import ComposeResult
from textual.containers import Container 
from src.components.Lista.Lista import TablaCambios 
from src.backend.controllers.eventController import EventController 

class EventList(Container): 
    def __init__(self): 
        super().__init__() 
        self.tabla_eventos=TablaCambios("Eventos") 
        self.eventController = EventController() 
        
    def compose(self)->ComposeResult: 
        yield self.tabla_eventos 
    
    def _on_mount(self)-> None: 
        self.cargar_eventos() 
    
    def cargar_eventos(self): 
        response = self.eventController.getEvents() 
        
        if response["message"]=="Exito al Obtener los eventos": 
            eventos= response["data"] 
            self.tabla_eventos.data(eventos)
        else: 
            print("Error: ",response["message"]) 
    
    
    def cargar_evento_by_ID(self,id:int):
        response = self.eventController.getEventById(id)

        if response["message"]=="Exito al Obtener los eventos":
           evento= response["data"] 
           self.tabla_eventos.data(evento)
        else:
            print("Error: ",response["message"])