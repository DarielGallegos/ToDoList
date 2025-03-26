#Modelo de Datos de Tareas
class Tareas:
    def __init__(self, id:int = 0 , titulo:str = "", descripcion:str = "", prioridad:int = 0 , fecha_vencimiento:str = "",  estado:int = 1):
        self.id : int = id
        self.titulo : str = titulo
        self.descripcion : str = descripcion
        self.prioridad : int = prioridad
        self.fecha_vencimiento : str = fecha_vencimiento
        self.estado : int = estado