from src.backend.models.init import init_database
from src.backend.controllers.taskController import TaskController
from src.backend.controllers.eventController import EventController
from src.backend.models.data.task import Tareas
from src.backend.models.data.events import Events
if __name__ == "__main__":
   
    init_database()
  
    taskController = TaskController()
    eventController = EventController()

    # Crear Tarea y Evento
    task = Tareas(id=4, titulo="Tarea N", descripcion="Descripcion de la Tarea 1 Mod", prioridad=1, fecha_vencimiento="2024-01-01", estado=1)
    event = Events(id=3, titulo="Evento N", descripcion="Descripcion del Evento 1 Mod", ubicacion="Ubicacion del Evento 1", fecha_inicio="2021-10-10", fecha_final="2021-10-10", estado=1)
    print(taskController.getTasks())
    print(eventController.getEvents())
    print(taskController.createTask(task))
    print(eventController.createEvent(event))
    print(taskController.getTaskById(6))
    print(eventController.getEventById(3))
    
"""
    # Actualizar Tarea y Evento
    task = Tareas(id=4, titulo="Tarea 1", descripcion="Descripcion de la Tarea 1 Mod", prioridad=1, fecha_vencimiento="2024-01-01", estado=1)
    event = Events(id=2, titulo="Evento 1", descripcion="Descripcion del Evento 1 Mod", ubicacion="Ubicacion del Evento 1", fecha_inicio="2021-10-10", fecha_final="2021-10-10", estado=1)
    print(taskController.updateTask(task))
    print(eventController.updateEvent(event))
    print(taskController.getTasks())
    print(eventController.getEvents())

    # Eliminar Tarea y Evento
    print(taskController.getTasks())
    print(eventController.getEvents())
    print(taskController.deleteTask(4))
    print(eventController.deleteEvent(2))
    print(taskController.getTasks())
    print(eventController.getEvents())
"""