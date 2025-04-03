from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label, Button
from src.components.FormEvent.FormEvent import FormularioEvento, FormularioEventoMensaje
from src.backend.controllers.eventController import EventController
from src.backend.models.data.events import Events
from textual import events

class EventView(Container):
    def __init__(self, evento_id: int = None, parent_list=None):
        super().__init__()
        self.evento_id = evento_id 
        self.parent_list = parent_list
        self.event_controller = EventController()
        self.formulario = None
        self.modo = "edicion" if evento_id else "creacion" 

    def compose(self) -> ComposeResult:
        titulo = "EDITAR EVENTO" if self.modo == "edicion" else "REGISTRO DE EVENTO"
        yield Label(titulo, classes="titulo")

        self.formulario = FormularioEvento([
            {"id": "titulo", "label": "Título", "tipo": "texto", "placeholder": "Escriba un título", "max_length": 50, "requerido": True},
            {"id": "descripcion", "label": "Descripción", "tipo": "textarea", "requerido": False},
            {"id": "ubicacion", "label": "Ubicación", "tipo": "texto", "placeholder": "Escriba la ubicación", "requerido": True}, 
        ])
        yield self.formulario

    def on_mount(self):
        self.capture_key_events = True
        if self.modo == "edicion" and self.evento_id:
            self.cargar_datos_evento(self.evento_id)

    def volver_a_lista(self):
        if self.parent_list:
            self.parent_list.mostrar_tabla()
            self.remove() 
        else:
            from src.views.events.eventList import EventList
            container = self.app.query_one("#viewContainer") 
            container.remove_children()
            container.mount(EventList())
        
        self.app.set_focus(None) 
        if self.parent_list:
            self.call_after_refresh(self.parent_list.tabla_eventos.focus)

    def guardar_evento(self):
        self.formulario.enviar_datos() 

    def cargar_datos_evento(self, evento_id: int):
        try:
            response = self.event_controller.getEventById(evento_id)
            if response["message"] == "Exito al Obtener los eventos" and isinstance(response["data"], (tuple, list)):
                evento = response["data"]
                if len(evento) >= 6: 
                    self.formulario.inputs["titulo"].value = str(evento[1])
                    self.formulario.inputs["descripcion"].text = str(evento[2])
                    self.formulario.inputs["ubicacion"].value = str(evento[3])
                    self.formulario.calendario_inicio.selected_date = str(evento[4])
                    self.formulario.calendario_final.selected_date = str(evento[5])
        except Exception as e:
            self.notify(f"Error al cargar datos: {str(e)}", severity="error")

    def on_formulario_evento_mensaje(self, message: FormularioEventoMensaje):
        try:
            evento = Events(
                id=self.evento_id if self.modo == "edicion" else None,
                titulo=message.datos["titulo"],
                descripcion=message.datos["descripcion"],
                ubicacion=message.datos["ubicacion"],
                fecha_inicio=message.datos["fecha_inicio"],
                fecha_final=message.datos["fecha_final"]
            )

            if self.modo == "edicion":
                self.event_controller.updateEvent(evento) 
            else:
                self.event_controller.createEvent(evento)  
            
            if self.parent_list:
                self.parent_list.mostrar_tabla()
            else:
                self.volver_a_lista()
            
        except Exception as e:
            pass

    def on_key(self, event: events.Key) -> None:
        if event.key == "ctrl+b":
            self.volver_a_lista()