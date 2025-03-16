from src.app import ToDoList
from src.backend.models.init import init_database
if __name__ == "__main__":
    init_database()
    ToDoList().run()
    