from textual.widget import Widget 
from textual.widgets import Input, Label, Button, TextArea, Select
from textual.message import Message
from textual.containers import Container, ScrollableContainer
import re
from datetime import datetime
from src.components.buttons.send_button import Send_button

from src.components.calendar.calendario import Calendario


class FormularioMensaje(Message):
    def __init__(self, datos: dict) -> None:
        super().__init__()
        self.datos = datos  # Diccionario con los valores del formulario

class FormularioInput(Widget):
    def __init__(self, campos, boton_texto="Enviar"):
        super().__init__()
        self.campos = campos 
        self.boton_texto = boton_texto
        self.inputs = {}  

    def compose(self):
        with Container():
            with ScrollableContainer(id="formulario_task", classes="formulario-task"):
                for campo in self.campos:
                    if campo["id"] in ["titulo", "descripcion"]:
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

                with Container(classes="campo-contenedor"):
                    yield Label("Prioridad:", classes="campo-label")
                    self.select_prioridad = Select(
                        options=[
                            ("Selecciona tu prioridad", ""),
                            ("Urgente e Importante", "Urgente e Importante"),
                            ("Importante pero no Urgente", "Importante pero no Urgente"),
                            ("Urgente pero no Importante", "Urgente pero no Importante"),
                            ("Ni Importante ni Urgente", "Ni Importante ni Urgente")
                        ],
                        value="",
                        classes="campo-select"
                    )
                    yield self.select_prioridad

                with Container(classes="fecha-venci-contenedor"):
                    yield Label("Fecha de Vencimiento:", classes="campo-label")
                    self.calendario_vencimiento = Calendario()
                    yield self.calendario_vencimiento

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

        for campo in self.campos:
            input_widget = self.inputs[campo["id"]]
            contenedor = input_widget.parent  
            contenedor.remove_class("error") 

        # Validaciones
        for campo in self.campos:
            input_widget = self.inputs[campo["id"]]
            valor = input_widget.text if isinstance(input_widget, TextArea) else input_widget.value
            contenedor = input_widget.parent  

            if campo.get("requerido", False) and not valor.strip():
                self.notify(f"El campo '{campo['label']}' no puede estar vacío.", severity="error")
                contenedor.add_class("error")
                errores = True
        
            if campo.get("validacion"):
                if not re.match(campo["validacion"], valor):
                    self.notify(f"{campo['mensaje_error']}", severity="error")
                    contenedor.add_class("error")
                    errores = True

        if not self.calendario_vencimiento.selected_date:
            self.notify("Debe seleccionar una fecha de vencimiento.", severity="error")
            errores = True
        
        if not self.select_prioridad.value:
            self.notify("Debe seleccionar una prioridad.", severity="error")
            errores = True
            
        if not errores:
            datos["fecha_vencimiento"] = self.calendario_vencimiento.selected_date
            datos["prioridad"] = self.select_prioridad.value

            for campo in self.campos:
                input_widget = self.inputs[campo["id"]]
                valor = input_widget.text if isinstance(input_widget, TextArea) else input_widget.value
                datos[campo["id"]] = valor

            self.post_message(FormularioMensaje(datos))

            for campo in self.campos:
                input_widget = self.inputs[campo["id"]]
                if isinstance(input_widget, TextArea):
                    input_widget.text = "" 
                else:
                    input_widget.value = ""  

            self.calendario_vencimiento.selected_date = None
            self.calendario_vencimiento.selected_date_label.update("Selecciona una fecha")
            self.calendario_vencimiento.reset_calendar()
            self.select_prioridad.value = ""

            list(self.inputs.values())[0].focus()
            self.notify("✔️ Tarea guardada correctamente.", severity="success")
   
    def set_values(self, values: dict):
        """Establece los valores del formulario"""
        for field_id, value in values.items():
            if field_id in self.inputs:
                input_widget = self.inputs[field_id]
                if isinstance(input_widget, TextArea):
                    input_widget.text = value
                else:
                    input_widget.value = value
