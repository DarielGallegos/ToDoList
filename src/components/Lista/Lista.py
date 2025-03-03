from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button,Label,ListView,ListItem


class TablaCambios(App):
    CSS_PATH = "../../css/try.tcss"
    def compose(self) -> ComposeResult:

        #Lista
        self.items = ["Churro","Banana","Zanahoría"]
        self.list_view = ListView(*[ListItem(Label(i)) for i in self.items])
        yield self.list_view
       
        #Intento

        self.selected_label= Label("Selected Item: None")
        yield self.selected_label
        #Botones
        with Horizontal(classes="box1"): 
            with Vertical(): 
                 yield Button("Actualizar",variant="success",disabled=False,id="btn_cambiar")
                 
            with Vertical(): 
                yield Button("Eliminar",variant="error",disabled=False, id="btn_eliminar") 
            
            with Vertical(): 
                 yield Button("Ordenar",variant="primary",disabled=False,id="btn_ordenar")
         
    #Actualizar lista
    def actualizar(self)->None:
        self.list_view.clear()
        for item in self.items:
            self.list_view.append(ListItem(Label(item)))

    #Onpressed
    def on_button_pressed(self, event: Button.Pressed) -> None: 

        #Ordenar
            if event.button.id == "btn_ordenar":
                self.items.sort()
                self.actualizar()
        #Eliminar
            elif event.button.id == "btn_eliminar":

                #Sacado de un foro documentación: https://github.com/Textualize/textual/discussions/1840
                selecteds = self.list_view.index
                if selecteds is not None:
                    self.selected_label.update(f"Selección: {self.items[selecteds]}")
                    del self.items[selecteds]
                    self.actualizar()
        #Cambiar - Le falta
            elif event.button.id == "btn_cambiar":
                selecteds = self.list_view.index
                if selecteds is not None:
                    self.items[selecteds] += " (Updated)"
                    self.actualizar()


if __name__ == "__main__":
    app = TablaCambios()
    app.run()