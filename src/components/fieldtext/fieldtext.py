from textual.widget import Widget
from textual.widgets import Input, Label, Button,TextArea
from textual.message import Message
from textual.containers import Container
import re
from datetime import datetime


class FormularioMensaje(Message):
    def __init__(self, titulo: str, descripcion: str, fecha: str) -> None:
        super().__init__()  
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha = fecha
        self.ultimo_texto_valido = ""
        self.ultima_posicion_seleccion = (0, 0)

class FormularioInput(Widget):
    def compose(self):
        
        with Container(id="formulario", classes="formulario"):
            with Container(classes="campo-contenedor"):
                yield Label("Título:", classes="campo-label")
                self.titulo = Input(placeholder="Escriba un título", classes="campo-input")
                yield self.titulo

            with Container(classes="descripcion-contenedor"):
                yield Label("Descripción:", classes="campo-label")
                self.descripcion = TextArea(
                text="", 
                classes="campo-textarea",
                language="markdown",
                id="descripcion",
                show_line_numbers=False
            )
                yield self.descripcion

            with Container(classes="campo-contenedor"):
                yield Label("Fecha:", classes="campo-label")
                self.fecha = Input(placeholder="DD/MM/YYYY", classes="campo-input")
                yield self.fecha

            with Container(classes="contenedor-boton"):
                yield Button("Enviar", id="boton-enviar")

    def on_mount(self):
            
        self.titulo.focus()

    def on_input_changed(self, event: Input.Changed):
        input = event.input
        value = input.value
        
        if input == self.titulo:
            if len(value) > 50:
                input.value = value[:50]
        elif input == self.fecha:
            if len(value) > 10:
                input.value = value[:10]

    def on_text_area_changed(self, event: TextArea.Changed):
        if event.text_area == self.descripcion:
            if len(event.text_area.text) > 200:

                event.text_area.text = self.ultimo_texto_valido
                event.text_area.selection = self.ultima_posicion_seleccion
            else:
                self.ultimo_texto_valido = event.text_area.text
                self.ultima_posicion_seleccion = event.text_area.selection

    def on_button_pressed(self, event: Button.Pressed):
        
        contenedores = self.query(".campo-contenedor")
        for contenedor in contenedores:
            contenedor.remove_class("error")
            
        errores = False

        if not self.titulo.value.strip():
            contenedores[0].add_class("error")
            self.notify("El título no puede estar vacío.", severity="error")
            errores = True 

        if not re.match(r"^\d{2}/\d{2}/\d{4}$", self.fecha.value):
            contenedores[1].add_class("error")
            self.notify("Formato DD/MM/YYYY", severity="error")
            errores = True
        else:
            try:
                datetime.strptime(self.fecha.value, "%d/%m/%Y")
            except ValueError:            
                contenedores[1].add_class("error")
                self.notify("Fecha inválida. Verifique el día, mes o año.", severity="error")
                errores = True

        if not errores:
            self.post_message(FormularioMensaje(
                self.titulo.value, 
                self.descripcion.text,  
                self.fecha.value
            ))

            self.titulo.value = ""
            self.descripcion.text = ""
            self.fecha.value = ""
            self.titulo.focus()

            self.notify("Formulario enviado correctamente.", severity="success")
