from textual.widget import Widget
from textual.widgets import Input, Label, Button, TextArea
from textual.message import Message
from textual.containers import Container, ScrollableContainer
import re
from datetime import datetime
from src.components.buttons.send_button import Send_button
from src.components.calendar.calendario import Calendario

class FormularioEventoMensaje(Message):
    def __init__(self, datos: dict) -> None:
        super().__init__()
        self.datos = datos

class FormularioEvento(Widget):
    def __init__(self, campos, boton_texto="Crear Evento"):
        super().__init__()
        self.campos = campos
        self.boton_texto = boton_texto
        self.inputs = {}
        
    def compose(self):
        with Container():  
            with ScrollableContainer(id="formulario_evento", classes="formulario-evento"):
                for campo in self.campos:
                    if campo["id"] in ["titulo", "descripcion", "ubicacion"]:
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

                with Container(classes="fechas-contenedor"):
                    with Container(classes="fecha-contenedor"):
                        yield Label("Fecha Inicio:", classes="campo-label")
                        self.calendario_inicio = Calendario()
                        yield self.calendario_inicio

                    with Container(classes="fecha-contenedor"):
                        yield Label("Fecha Final:", classes="campo-label")
                        self.calendario_final = Calendario()
                        yield self.calendario_final

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

        if not self.calendario_inicio.selected_date:
            self.notify("Debe seleccionar una fecha de inicio.", severity="error")
            errores = True

        if not self.calendario_final.selected_date:
            self.notify("Debe seleccionar una fecha final.", severity="error")
            errores = True

        if self.calendario_inicio.selected_date and self.calendario_final.selected_date:
            formato_fecha = "%Y-%m-%d" 
            fecha_inicio = datetime.strptime(self.calendario_inicio.selected_date, formato_fecha)
            fecha_final = datetime.strptime(self.calendario_final.selected_date, formato_fecha)

            if fecha_final < fecha_inicio:
                self.notify("La fecha final no puede ser inferior a la fecha de inicio.", severity="error")
                errores = True

        if not errores:
            datos["fecha_inicio"] = self.calendario_inicio.selected_date
            datos["fecha_final"] = self.calendario_final.selected_date

            for campo in self.campos:
                input_widget = self.inputs[campo["id"]]
                valor = input_widget.text if isinstance(input_widget, TextArea) else input_widget.value
                datos[campo["id"]] = valor

            self.post_message(FormularioEventoMensaje(datos))

            for campo in self.campos:
                input_widget = self.inputs[campo["id"]]
                if isinstance(input_widget, TextArea):
                    input_widget.text = "" 
                else:
                    input_widget.value = ""  

            self.calendario_inicio.selected_date = None
            self.calendario_inicio.selected_date_label.update("Selecciona una fecha")
            self.calendario_inicio.reset_calendar()

            self.calendario_final.selected_date = None
            self.calendario_final.selected_date_label.update("Selecciona una fecha")
            self.calendario_final.reset_calendar()

            list(self.inputs.values())[0].focus()     
            self.notify("✔️ Evento guardado correctamente.", severity="success")

    def set_values(self, values: dict):
        """Establece los valores del formulario"""
        for field_id, value in values.items():
            if field_id in self.inputs:
                input_widget = self.inputs[field_id]
                if isinstance(input_widget, TextArea):
                    input_widget.text = value
                else:
                    input_widget.value = value