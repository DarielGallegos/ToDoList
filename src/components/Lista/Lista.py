from rich.text import Text
from datetime import datetime
from src.components.Lista import estilo
from textual.widgets import DataTable, Static
from textual.app import ComposeResult, Widget
from textual.containers import VerticalScroll

class TablaCambios(Widget):    
    def __init__(self, tipo: str):
        super().__init__()
        self.tipo = tipo
        self.table = DataTable()
        self.row_keys = []

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Static(f"GESTION DE {self.tipo.upper()}", classes="titulo")
            yield self.table
    
    def on_mount(self) -> None:
        self.theme = estilo.arctic_theme  
        self.theme = "Tabla"

        self.table = self.query_one(DataTable)
        self.table.zebra_stripes = 1
        self.table.header_height = 1

        if self.tipo.upper() == "EVENTOS":
            headers = ["N°", "Título", "Descripción", "Ubicación", "Inicio", "Fin", "Actualizar", "Eliminar"]
        elif self.tipo.upper() == "TAREAS":
            headers = ["N°", "Título", "Descripción", "Prioridad", "Vencimiento", "Actualizar", "Eliminar"]
        
        header_row = [Text(f" {col} \n  ", style="bold", justify="center") for col in headers]
        self.table.add_columns(*header_row)

    def data(self, casos) -> None:
        self.row_keys = []
        self.table.clear()
        
        if self.tipo.upper() == "EVENTOS":
            sorted_rows = sorted(casos, key=lambda caso: datetime.strptime(caso[4], "%Y-%m-%d"))
            for caso in sorted_rows:
                descripcion = caso[2][:20] + "..." if len(caso[2]) > 25 else caso[2]
                fila = [
                    Text(str(caso[0]), justify="center", style="italic"),
                    Text(caso[1], justify="left", style="italic"),
                     Text(descripcion, justify="left", style="italic"),
                    Text(caso[3], justify="left", style="italic"),
                    Text(caso[4][:10], justify="center", style="italic"),
                    Text(caso[5][:10], justify="center", style="italic"),
                    Text("🔂"[:1], justify="center"),
                    Text("❌"[:1], justify="center"), 
                ]
                key = f"row-{str(caso[0])}"
                self.table.add_row(*fila, key=key)
                self.row_keys.append(key)
            self.table.refresh()

        elif self.tipo.upper() == "TAREAS":
            sorted_rows = sorted(casos, key=lambda caso: datetime.strptime(caso[4], "%Y-%m-%d"))
            for caso in sorted_rows:
                descripcion = caso[2][:25] + "..." if len(caso[2]) > 25 else caso[2]
                fila = [
                    Text(str(caso[0]), justify="center", style="italic"),
                    Text(caso[1], justify="left", style="italic"),
                    Text(descripcion, justify="left", style="italic"),
                    Text(str(caso[3]), justify="left", style="italic"),
                    Text(caso[4][:12], justify="center", style="italic"),
                    Text("🔂"[:1], justify="center"),
                    Text("❌"[:1], justify="center"), 
                ]
                key = f"row-{str(caso[0])}"
                self.table.add_row(*fila, key=key)
                self.row_keys.append(key)
            self.table.refresh()

    def on_data_table_cell_selected(self, event: DataTable.CellSelected) -> None:
        row, col = event.coordinate

        if self.tipo.upper() == "EVENTOS":
            if col == 7:  
                key_to_remove = self.row_keys[row]
                self.table.remove_row(key_to_remove)
                self.row_keys = [key for idx, key in enumerate(self.row_keys) if idx != row]
        if self.tipo.upper() == "TAREAS":
            if col == 6:  
                key_to_remove = self.row_keys[row]
                self.table.remove_row(key_to_remove)
                self.row_keys = [key for idx, key in enumerate(self.row_keys) if idx != row]
        