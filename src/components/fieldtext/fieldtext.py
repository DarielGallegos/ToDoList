from textual.widget import Widget
from textual.widgets import Input, Label, Button, TextArea
from textual.message import Message
from textual.containers import Container
import re
from datetime import datetime
from src.components.buttons.send_button import Send_button


class FormularioMensaje(Message):
    def __init__(self, datos: dict) -> None:
        super().__init__()
        self.datos = datos  # Diccionario con los valores del formulario

class FormularioInput(Widget):
    def __init__(self, campos, boton_texto="Enviar"):
        super().__init__()
        self.campos = campos  # Lista de campos con configuración
        self.boton_texto = boton_texto
        self.inputs = {}  # Almacena referencias a los inputs

    def compose(self):
        with Container(id="formulario", classes="formulario"):
            for campo in self.campos:
                with Container(classes="campo-contenedor"):
                    yield Label(campo["label"] + ":", classes="campo-label")
                    
                    if campo["tipo"] == "textarea":
                        input_widget = TextArea(
                            text="", classes="campo-textarea", id=campo["id"],
                            language="markdown", show_line_numbers=False
                        )
                    else:
                        input_widget = Input(placeholder=campo.get("placeholder", ""), classes="campo-input")
                    
                    self.inputs[campo["id"]] = input_widget
                    yield input_widget
            
            with Container(classes="contenedor-boton"):
                yield Send_button()
    
    def on_mount(self):
        if self.inputs:
            list(self.inputs.values())[0].focus()
    
    def on_input_changed(self, event: Input.Changed):
        input = event.input
        for campo in self.campos:
            if self.inputs[campo["id"]] == input:
                if "max_length" in campo and len(input.value) > campo["max_length"]:
                    input.value = input.value[:campo["max_length"]]
    
    def on_button_pressed(self, event: Button.Pressed):
        errores = False
        datos = {}

        # Primero, limpiar errores anteriores
        for campo in self.campos:
            input_widget = self.inputs[campo["id"]]
            contenedor = input_widget.parent  # Obtener el contenedor del input
            contenedor.remove_class("error")  # Quitar la clase error si estaba

        # Validaciones
        for campo in self.campos:
            input_widget = self.inputs[campo["id"]]
            valor = input_widget.text if isinstance(input_widget, TextArea) else input_widget.value
            contenedor = input_widget.parent  # Obtener el contenedor del input
            
            if campo.get("requerido", False) and not valor.strip():
                self.notify(f"El campo '{campo['label']}' no puede estar vacío.", severity="error")
                contenedor.add_class("error")  # Agregar la clase de error
                errores = True
            
            if campo.get("validacion"):
                if not re.match(campo["validacion"], valor):
                    self.notify(f"{campo['mensaje_error']}", severity="error")
                    contenedor.add_class("error")
                    errores = True
            
            if campo.get("tipo") == "fecha":
                try:
                    datetime.strptime(valor, "%d/%m/%Y")
                except ValueError:
                    self.notify(f"Fecha inválida en '{campo['label']}'. Formato esperado: DD/MM/YYYY", severity="error")
                    contenedor.add_class("error")
                    errores = True
            
            datos[campo["id"]] = valor

        # Si no hay errores, enviar el mensaje y limpiar el formulario
        if not errores:
            self.post_message(FormularioMensaje(datos))
            for campo in self.campos:
                input_widget = self.inputs[campo["id"]]
                input_widget.value = "" if isinstance(input_widget, Input) else ""
            list(self.inputs.values())[0].focus()
            self.notify("Formulario enviado correctamente.", severity="success")

