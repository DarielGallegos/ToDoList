from src.backend.models.data.task import Tareas
from src.backend.models.contracts.tareasContract import TareasContract
class TaskController():
    def __init__(self):
        self.tareasContract = TareasContract()
    
    def getTasks(self) -> dict:
        request = self.tareasContract.select()
        response = {
            "message": "Exito al Obtener las tareas" if request["status"] else "Error al obtener las tareas",
            "data": request["data"]
        }
        return response
    
    def getTaskById(self, id:int) -> dict:
        request = self.tareasContract.selectById(id)
        response = {
            "message": "Exito al Obtener la tarea" if request["status"] else "Error al obtener la tarea",
            "data": request["data"]
        }
        return response
    
    def createTask(self, task:Tareas) -> dict:
        request = self.tareasContract.insert(task)
        response = {
            "message": "Exito al Insertar la tarea" if request["status"] else "Error al insertar la tarea",
            "data": request["data"]
        }
        return response
    
    def updateTask(self, task:Tareas) -> dict:
        request = self.tareasContract.update(task)
        response = {
            "message": "Exito al Actualizar la tarea" if request["status"] else "Error al actualizar la tarea",
            "data": request["data"]
        }
        return response
    
    def deleteTask(self, id:int) -> dict:
        request = self.tareasContract.delete(id)
        response = {
            "message": "Exito al Eliminar la tarea" if request["status"] else "Error al eliminar la tarea",
            "data": request["data"]
        }
        return response