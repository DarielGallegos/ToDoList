from textual.widget import Widget
from textual.widgets import Input, Label, Button
from textual.message import Message
from textual.containers import Container
import re
from datetime import datetime


class FormularioMensaje(Message):
    def __init__(self, titulo: str, descripcion: str, fecha: str) -> None:
        super().__init__()  # Llamar primero al constructor sin argumentos
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha = fecha

class FormularioInput(Widget):

    CSS_PATH = "src/css/input.tcss"

    def compose(self):
        
        with Container(id="formulario", classes="formulario"):
            with Container(classes="campo"):
                yield Label("Título:")
                self.titulo = Input(placeholder="escriba un titulo", classes="input")
                yield self.titulo

            with Container(classes="campo"):
                yield Label("Descripción:")
                self.descripcion = Input(placeholder="Máx. 100 caracteres", classes="input")
                yield self.descripcion

            with Container(classes="campo"):
                yield Label("Fecha (DD/MM/YYYY):")
                self.fecha = Input(placeholder="Ej: 15/12/2025", classes="input")
                yield self.fecha

            yield Button("Enviar", id="enviar", classes="boton")

    def on_button_pressed(self, event: Button.Pressed):
        
        errores = False

        if not self.titulo.value.strip():
            self.titulo.styles.border = ("heavy", "red")
            self.notify("El título no puede estar vacío.", severity="error")
            errores = True
        else:
            self.titulo.styles.border = ("none", "white")

        if len(self.descripcion.value) > 100:
            self.descripcion.styles.border = ("heavy", "red")
            self.notify("La descripción no puede superar los 100 caracteres.", severity="error")
            errores = True
        else:
            self.descripcion.styles.border = ("none", "white")

        if not re.match(r"^\d{2}/\d{2}/\d{4}$", self.fecha.value):
            self.fecha.styles.border = ("heavy", "red")
            self.notify("Formato de fecha inválido. Use DD/MM/YYYY.", severity="error")
            errores = True
        else:
            try:
                datetime.strptime(self.fecha.value, "%d/%m/%Y")
                self.fecha.styles.border = ("none", "white")
            except ValueError:
                self.fecha.styles.border = ("heavy", "red")
                self.notify("Fecha inválida. Verifique el día, mes o año.", severity="error")
                errores = True

        if not errores:
            self.post_message(
                FormularioMensaje(  
                    self.titulo.value, 
                    self.descripcion.value,  
                    self.fecha.value 
                )
            )
            self.notify("Formulario enviado correctamente.", severity="success")