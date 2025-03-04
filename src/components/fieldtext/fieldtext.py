from textual.widget import Widget
from textual.widgets import Input, Label, Button
from textual.message import Message
from textual.containers import Container, Horizontal

class MensajeAccion(Message):
    def __init__(self, nombre: str, accion: str) -> None:
        super().__init__()
        self.nombre = nombre
        self.accion = accion

class NombreInput(Widget):
    CSS_PATH = "src/css/input.tcss"

    def compose(self):
        with Container(id="formulario", classes="formulario"):
            yield Label("Nombre:")
            self.nombre = Input(placeholder="Ingrese su nombre", classes="input")
            yield self.nombre

            with Container(classes="botones"):
                yield Button("Guardar", id="guardar", classes="boton guardar")
                yield Button("Editar", id="editar", classes="boton editar")
                yield Button("Eliminar", id="eliminar", classes="boton eliminar")

    def on_button_pressed(self, event: Button.Pressed):
        if not self.nombre.value.strip():
            self.nombre.styles.border = ("heavy", "red")
            self.notify("El nombre no puede estar vacío.", severity="error")
            return
        else:
            self.nombre.styles.border = ("none", "white")

        if event.button.id == "guardar":
            self.accion("Guardado", "Nombre guardado exitosamente.", "success")
        elif event.button.id == "editar":
            self.accion("Editado", "Nombre editado correctamente.", "info")
        elif event.button.id == "eliminar":
            self.accion("Eliminado", "Nombre eliminado correctamente.", "warning")

    def accion(self, tipo: str, mensaje: str, severidad: str):
        self.post_message(MensajeAccion(self.nombre.value, tipo))
        self.notify(mensaje, severity=severidad)
