import sqlite3

class RepositoryDB:
    def __init__(self):
        try:
            sqlite3.threadsafety = 1
            self.conn = sqlite3.connect('todolist.db3')
        except sqlite3.Error as e:
            print("Error SQLITE: ",e)

    def getConnect(self):
        return self.conn