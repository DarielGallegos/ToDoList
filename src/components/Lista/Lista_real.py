from textual.widgets import DataTable,Static
from textual.app import App, ComposeResult, Widget
from textual.containers import VerticalScroll
from datetime import datetime
from rich.text import Text
from src.components.Lista import estilo

ROWS = [
    ("N°", "Titulo", "Descripción", "Fecha", "Actualizar", "Eliminar"),
    (1, "Informe", "Completar informe", "2025-04-12"),
    (2, "Código", "Revisar código", "2025-04-25"),
    (3, "Presentación", "Preparar presentación", "2025-04-07"),
    (4, "Correo", "Enviar correo de seguimientoseguimientoseguimiento", "2025-04-20"),
    (5, "Reunión", "Reunión de equipo", "2025-04-10"),
    (6, "Base de datos", "Actualizar base de datos", "2025-04-22"),
    (7, "Propuestas", "Revisar propuestas", "2025-04-28"),
    (8, "Reporte", "Redactar reporte", "2025-04-15"),
    (9, "Análisis", "Hacer análisis de mercado", "2025-04-05"),
    (10, "Resultados", "Verificar resultados", "2025-04-18"),
]

class TablaCambios(Widget):    
    def __init__(self, tipo: str):
        super().__init__()
        self.tipo = tipo

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Static(f"GESTION DE {self.tipo.upper()}", classes="titulo")
            yield DataTable()
      
    
    def on_mount(self)->None:

        #Estilo
        self.theme = estilo.arctic_theme  
        self.theme = "Tabla"

        #Tabla
        Tabla= self.table = self.query_one(DataTable)
        Tabla.zebra_stripes=1
        Tabla.header_height=1

        #Encabezados
        header_row = [Text(f" {col} \n  ", style="bold #03AC13 white 20", justify="center") for col in ROWS[0]]
        Tabla.add_columns(*header_row)

        #Filas
        self.row_keys = []
        sorted_rows = sorted(ROWS[1:], key=lambda row: datetime.strptime(row[3], "%Y-%m-%d"))

        for row in sorted_rows:
            styled_row = [ Text(f" {cell} \n  ", style="bold #03AC13 16", justify="left") if idx in [0, 1]  
                            else Text(f" {str(cell)[:20]}... \n  ", style="bold #03AC13 16", justify="left") if idx == 2 
                            else Text(f" {cell} \n  ", style="bold #03AC13 16", justify="center") 
                            for idx, cell in enumerate(row)]
            
            styled_row.extend([Text("🔂", style="bold #03AC13 16", justify="center"),
                               Text("❌", style="bold #03AC13 16", justify="center")])
            
            key = f"row-{row[0]}"
            
            Tabla.add_row(*styled_row, key=key)

            self.row_keys.append(key)
   

    #Selección de celdas y eliminar
    def on_data_table_cell_selected(self, event: DataTable.CellSelected) -> None:
        #Basicamente al combinar row y col se crea una coordenada, lo que son las celdas
        row, col = event.coordinate
        
        #Luego cuando se verifique que presionamos la columna 4 "Eliminiar"
        #Se procede a eliminar por medio de la KEY que sería como el index de nuestra fila
        #esto debido a que Textual es sensible y le duele que le digan las cosas como son :D
        if col == 5 :
            key_to_remove = self.row_keys[row]
            self.table.remove_row(key_to_remove)

            #Luego reiniamos la lista de keys ya que eliminamos una o varias.
            self.row_keys = [key for idx, key in enumerate(self.row_keys) if idx != row] 

           
