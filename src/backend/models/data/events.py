#Modelo de Datos de Eventos
class Events:
    def __init__(self, id : int = 0, titulo : str = "", descripcion : str = "", ubicacion : str = "", fecha_inicio : str = "", fecha_final : str = "", estado : str = ""):
        self.id : int = id
        self.titulo : str = titulo
        self.descripcion : str = descripcion    
        self.ubicacion : str = ubicacion
        self.fecha_inicio : str = fecha_inicio
        self.fecha_final : str = fecha_final
        self.estado : int = estado