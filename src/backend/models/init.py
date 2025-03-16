from models.contracts.eventsContract import EventContract
from models.contracts.tareasContract import TareasContract
from models.contracts.estadosContract import EstadosContract
from models.contracts.prioridadesContract import PrioridadesContract
from models.data.task import Tareas
def init_tables():
    # Crear Tablas en la Base de Datos
    PrioridadesContract().createTable()
    EstadosContract().createTable()
    EventContract().createTable()
    TareasContract().createTable()