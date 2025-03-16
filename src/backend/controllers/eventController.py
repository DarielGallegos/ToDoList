from src.backend.models.data.events import Events
from src.backend.models.contracts.eventsContract import EventContract
class EventController:
    def __init__(self):
        self.eventContract = EventContract()
    
    def getEvents(self) -> dict:
        request = self.eventContract.select()
        response = {
            "message": "Exito al Obtener los eventos" if request["status"] else "Error al obtener los eventos",
            "data": request["data"]
        }
        return response
    
    def getEventById(self, id:int) -> dict:
        request = self.eventContract.selectById(id)
        response = {
            "message": "Exito al Obtener los eventos" if request["status"] else "Error al obtener los eventos",
            "data": request["data"]
        }
        return response
    
    def createEvent(self, event:Events) -> dict:
        request = self.eventContract.insert(event)
        response = {
            "message": "Exito al Insertar el evento" if request["status"] else "Error al insertar el evento",
            "data": request["data"]
        }
        return response
    
    def updateEvent(self, event:Events) -> dict:
        request = self.eventContract.update(event)
        response = {
            "message": "Exito al Actualizar el evento" if request["status"] else "Error al actualizar el evento",
            "data": request["data"]
        }
        return response
    
    def deleteEvent(self, id:int) -> dict:
        request = self.eventContract.delete(id)
        response = {
            "message": "Exito al Eliminar el evento" if request["status"] else "Error al eliminar el evento",
            "data": request["data"]
        }
        return response