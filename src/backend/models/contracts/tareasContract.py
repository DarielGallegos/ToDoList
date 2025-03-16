import sqlite3
from repositories.connect.repositoryDB import RepositoryDB
from models.data.task import Tareas
class TareasContract(RepositoryDB):
    __table__ = "tareas"
    __attributes__ = {
        "id" : ["id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
        "titulo" : ["titulo", "TEXT NOT NULL"],
        "descripcion" : ["descripcion", "TEXT NOT NULL"],
        "prioridad" : ["prioridad", "INTEGER NOT NULL"],
        "fecha_vencimiento" : ["fecha_vencimiento", "DATE NOT NULL"],
        "estado" : ["estado", "INTEGER NOT NULL"]
    }
    __relations__ = {
        "fk_prioridad" : f"FOREIGN KEY({__attributes__['prioridad'][0]}) REFERENCES prioridades(id)",
        "fk_estado" : f"FOREIGN KEY({__attributes__['estado'][0]}) REFERENCES estados(id)"
    }

    def __init__(self):
        super().__init__()

    def createTable(self):
        try:
            cur = self.conn.cursor()
            query = f"CREATE TABLE IF NOT EXISTS {self.__table__} ("
            for key in self.__attributes__:
                query += f"{self.__attributes__[key][0]} {self.__attributes__[key][1]}, "
            for key in self.__relations__:
                query += f"{self.__relations__[key]}, "
            query = query[:-2]
            query += ")"
            cur.execute(query)
            self.conn.commit()
            cur.close()
        except sqlite3.Error as e:
            print(e)
    
    def select(self) -> dict:
        try:
            cur = self.conn.cursor()
            query = f"SELECT * FROM {self.__table__}"
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()
            return {"status": True, "data":rows}
        except sqlite3.Error as e:
            print(e)
            return {"status": False, "data":[]}
    
    def selectById(self, id:int) -> dict:
        try:
            cur = self.conn.cursor()
            query = f"SELECT * FROM {self.__table__} WHERE id = {id}"
            cur.execute(query)
            row = cur.fetchone()
            cur.close()
            return {"status":True, "data":row}
        except sqlite3.Error as e:
            print(e)
            return {"status":False, "data":[]}

    def insert(self, task: Tareas) -> dict:
        try:
            cur = self.conn.cursor()
            query = f"INSERT INTO {self.__table__} ("
            for key in self.__attributes__:
                if key != "id":
                    query += f"{self.__attributes__[key][0]}, "
            query = query[:-2]
            query += ") VALUES ("
            for key in self.__attributes__:
                if key != "id":
                    query += f"'{getattr(task, key)}', "
            query = query[:-2]
            query += ")"
            cur.execute(query)
            self.conn.commit()
            cur.close()
            return {"status":True }
        except sqlite3.Error as e:
            print(e)
            return {"status":False }
    
    def update(self, task: Tareas) -> dict:
        try:
            cur = self.conn.cursor()
            query = f"UPDATE {self.__table__} SET "
            for key in self.__attributes__:
                query += f"{self.__attributes__[key][0]} = '{getattr(task, key)}', "
            query = query[:-2]
            query += f" WHERE id = {task.id}"
            cur.execute(query)
            self.conn.commit()
            cur.close()
            return {"status":True }
        except sqlite3.Error as e:
            print(e)
            return {"status":False }
    
    def delete(self, id:int) -> dict:
        try:
            cur = self.conn.cursor()
            query = f"DELETE FROM {self.__table__} WHERE id = {id}"
            cur.execute(query)
            self.conn.commit()
            cur.close()
            return {"status":True }
        except sqlite3.Error as e:
            print(e)
            return {"status":False }