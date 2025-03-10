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
    CSS_PATH = "src/css/main.tcss"

    def compose(self):
        with Container(id="formulario", classes="formulario"):
            yield Label("Nombre:")
            self.nombre = Input(placeholder="Ingrese su nombre", classes="input")
            yield self.nombre

            with Horizontal(classes="botones"):
                yield Button("Guardar", id="guardar", classes="botonGuardar")
                yield Button("Editar", id="editar", classes="botonEditar")
                yield Button("Eliminar", id="eliminar", classes="botonEliminar")

    def on_button_pressed(self, event: Button.Pressed):
        if not self.nombre.value.strip():
            self.nombre.styles.border = ("heavy", "red")
            self.notify("⚠️ El nombre no puede estar vacio.", severity="error")
            self.mostrar_mensaje_error(event.button.id)  
            return
        else:
            self.nombre.styles.border = ("none", "white")

        if event.button.id == "guardar":
            self.accion("Guardado", "✅ Nombre guardado exitosamente.", "success")
        elif event.button.id == "editar":
            self.accion("Editado", "✏️ Nombre editado correctamente.", "info")
        elif event.button.id == "eliminar":
            self.accion("Eliminado", "🗑️ Nombre eliminado correctamente.", "warning")

    def accion(self, tipo: str, mensaje: str, severidad: str):
        self.post_message(MensajeAccion(self.nombre.value, tipo))
        self.notify(mensaje, severity=severidad)

    def mostrar_mensaje_error(self, accion: str):
        acciones = {
            "guardar": "Hubo un error al guardar.",
            "editar": "Hubo un error al editar.",
            "eliminar": "Hubo un error al eliminar.",
        }
        mensaje_error = acciones.get(accion, "Hubo un error desconocido.")
        self.notify(f"❌ {mensaje_error}", severity="error")