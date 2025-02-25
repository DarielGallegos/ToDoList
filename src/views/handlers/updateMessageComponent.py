from textual.message import Message

class UpdateMessageContainer(Message):
    
    def __init__(self, option: str) -> None:
        super().__init__()
        self.option = option
    
    @property
    def text(self) -> str:
        return self.option
