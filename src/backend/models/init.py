from src.backend.models.contracts.eventsContract import EventContract
from src.backend.models.contracts.tareasContract import TareasContract
from src.backend.models.contracts.estadosContract import EstadosContract
from src.backend.models.contracts.prioridadesContract import PrioridadesContract
def init_database():
    # Crear Tablas en la Base de Datos
    PrioridadesContract().createTable()
    EstadosContract().createTable()
    EventContract().createTable()
    TareasContract().createTable()