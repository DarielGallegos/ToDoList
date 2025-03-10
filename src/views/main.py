from textual.containers import VerticalScroll, Container
from textual.app import ComposeResult
from src.components.menu.Menu import Menu, TreeSelectionMessage
from src.views.tasks.tasksView import TaskView
from src.views.tasks.taskList import TaskList
from src.views.events.eventView import EventView

class Views(Container):
    
    viewContainer : VerticalScroll = VerticalScroll(id="viewContainer")
    __views = ["Crear Evento", "Listar Evento", "Crear Tarea", "Listar Tarea"]

    def compose(self) -> ComposeResult:
        yield Menu("Menu")
        yield self.viewContainer

    def on_tree_selection_message(self, message: TreeSelectionMessage):
        if f"{message.selected_option}" in self.__views:
            new_view = self.select_view(f"{message.selected_option}")
            if new_view:
                self.change_view(new_view)
        else:
            self.change_view(Container())

    
    def select_view(self, view: str):
        typeView = view.split(" ")[1]
        viewSpecific = view.split(" ")[0]
        if typeView == "Evento":
            if viewSpecific == "Crear":
                #return TaskView()
                return EventView()
            elif viewSpecific == "Listar":
                return TaskList()
        elif typeView == "Tarea":
            if viewSpecific == "Crear":
                return TaskView()
            elif viewSpecific == "Listar":
                return TaskList()
        
        return None
    
    def change_view(self, new_view):
        for child in list(self.viewContainer.children):
            child.remove()

        self.viewContainer.mount(new_view)