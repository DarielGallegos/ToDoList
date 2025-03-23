from datetime import datetime
from calendar import monthrange, month_name
from textual.containers import Vertical
from textual.widgets import DataTable, Label
from textual.widget import Widget


class Calendario(Widget):
    def __init__(self):
        super().__init__()
        self.month = datetime.now().month
        self.year = datetime.now().year
        self.selected_date_label = Label("Selecciona una fecha", classes="campo-fecha-label")  
        self.selected_date = None 
        self.calendario = None  
        
    def compose(self):
        with Vertical():
            self.titulo = Label(f"{month_name[self.month]} {self.year}", classes="titulo-calendario") #Widget para mostrar el label del mes y el label del año
            self.calendario = DataTable() #Widget de tabla para mostrar el calendario
            self.calendario.add_columns("L", "M", "X", "J", "V", "S", "D") #Columnas para la tabla con los dias de la semana 
            yield self.titulo
            yield self.calendario
            yield self.selected_date_label
            self.update()
    
    def update(self):
        if self.calendario is None: 
            return
        self.calendario.clear()
        init_month, total_days = monthrange(self.year, self.month) #init_moth guarda el dia de la semana en que inicia el mes y total_days guarda el total de dias del mes

        days = ["" for _ in range(init_month)] + [str(d) for d in range(1, total_days + 1)] #Es una lista de los dias del mes, se podria decir que los primeros elementos estan vacios para alinear las fechas en la tabla, para que despues esten seguifos de los dias del mes como cadenas

        for week in range(0, len(days), 7): #Hace la iteracion de la lista de las fechas en una incrementacion de 7 dias o sea la semana
            self.calendario.add_row(* days [week:week + 7]) #Hace el añadido de la fila a la tabla de los dias de la semana en el calendario
        self.titulo.update(f"{month_name[self.month]} {self.year}") #Permite actualizar el label que tiene el titulo del calendarios con los nombres de los meses y el año actual
    
    def reset_calendar(self):
        now = datetime.now()
        self.month = now.month
        self.year = now.year
        self.update()


    def on_data_table_cell_selected(self, event):
        row = event.coordinate.row  #Fila que esta seleccionada
        column = event.coordinate.column  #Columna que esta seleccionada
        cell = (row, column)  #Crear una tupla con las coordenadas de la celda
        day = self.calendario.get_cell_at(cell)  #Obtiene el valor de la celda seleccionada (ya es un str)

        if day.strip():  
            self.selected_date = datetime(self.year, self.month, int(day)).strftime("%Y-%m-%d")  #Formatea la fecha seleccionada
            self.selected_date_label.update(f"Fecha seleccionada: {self.selected_date}")  

    def on_key(self, event):
        if event.key == "ctrl+left":
            self.month = max(1, self.month - 1) #Para disminuir el mes de uno en uno, pero que tiene como limite que el mes no sea menor que uno
        elif event.key == "ctrl+right":
            self.month = min(12, self.month + 1) #Para aumentar el mes de uno en uno, pero que tiene como limite que el mes no sea mayor a doce
        self.update()
    