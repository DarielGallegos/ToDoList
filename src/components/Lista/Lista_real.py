from textual.app import App, ComposeResult
from textual.widgets import DataTable,Label
from textual.containers import Vertical
from datetime import datetime

ROWS = [
    ("Tarea", "Descripción", "Fecha", "Actualizar", "Eliminar"),
    (1, "Completar informe", "2025-04-12", "", ""),
    (2, "Revisar código", "2025-04-25", "", ""),
    (3, "Preparar presentación", "2025-04-07", "", ""),
    (4, "Enviar correo de seguimiento", "2025-04-20", "", ""),
    (5, "Reunión de equipo", "2025-04-10", "", ""),
    (6, "Actualizar base de datos", "2025-04-22", "", ""),
    (7, "Revisar propuestas", "2025-04-28", "", ""),
    (8, "Redactar reporte", "2025-04-15", "", ""),
    (9, "Hacer análisis de mercado", "2025-04-05", "", ""),
    (10, "Verificar resultados", "2025-04-18", "", ""),
]


class TablaCambios(App):
    def compose(self) -> ComposeResult:
        with Vertical():
            self.label = Label("Selecciona una celda")
            yield self.label
            yield DataTable()
      
    
    def on_mount(self)->None:
        self.table = self.query_one(DataTable)
        self.table.add_columns(*ROWS[0])
        
        #Orden por medio de columna 2 y sus paramentros de fecha -strptime-
        sorted_rows = sorted(ROWS[1:], key=lambda row: datetime.strptime(row[2], "%Y-%m-%d"))


        #Elemento key de las filas
        self.row_keys = []


        #Orden de Items
        for row in sorted_rows:
            tarea, descripcion, fecha, _, _ = row
            #En este caso elige el primer caracter de row que es el número de la tarea, por ello reconoce
            #dicho como la clave para eliminar
            key = f"row-{row[0]}"
            self.row_keys.append(key)
            self.table.add_row(tarea, descripcion, fecha, "Actualizar", "Eliminar",key=key)


    #Selección de celdas y eliminar
    def on_data_table_cell_selected(self, event: DataTable.CellSelected) -> None:
        #Basicamente al combinar row y col se crea una coordenada, lo que son las celdas
        row, col = event.coordinate
        self.label.update(f"Celda seleccionada: ({row}, {col})")
        
        #Luego cuando se verifique que presionamos la columna 4 "Eliminiar"
        #Se procede a eliminar por medio de la KEY que sería como el index de nuestra fila
        #esto debido a que Textual es sensible y le duele que le digan las cosas como son :D
        if col == 4 :
            self.label.update(f"Fila {row} eliminada")
            key_to_remove = self.row_keys[row]
            self.table.remove_row(key_to_remove)

            #Luego reiniamos la lista de keys ya que eliminamos una o varias.
            self.row_keys = [key for idx, key in enumerate(self.row_keys) if idx != row] 

        

           
if __name__ == "__main__":
    app = TablaCambios()
    app.run()