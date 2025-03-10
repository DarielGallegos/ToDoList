from textual.widgets import Button

class Send_button(Button):
    def __init__(self, label="Guardar"):
        super().__init__(label, id="boton-enviar")
