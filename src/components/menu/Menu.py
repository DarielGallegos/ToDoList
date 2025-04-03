from textual.app import ComposeResult
from textual.widgets import Tree, Label
from textual.message import Message

class TreeSelectionMessage(Message):

    def __init__(self,sender, option: str) -> None:
        self.option = option
        super().__init__()

    @property
    def selected_option(self) -> str:
        return self.option
    
class Menu(Tree[str]):
    # Definir widget global para el arbol
    tree : Tree[str] = Tree("Menu")

    def __init__(self, option: str) -> None:
        self.option = option
        super().__init__(self.option)

    def compose(self) -> ComposeResult:
		## Crea un arbol de opciones
        self.tree.root.expand()
        events = self.tree.root.add("Eventos", expand=True)
        task = self.tree.root.add("Tarea", expand=True)
        events.add_leaf("Crear Evento")
        events.add_leaf("Listar Evento")
        task.add_leaf("Crear Tarea")
        task.add_leaf("Listar Tarea")
        yield self.tree

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Maneja la selección de nodos en el árbol."""
        self.option = event.node.label
        self.post_message(TreeSelectionMessage(self, self.option))
