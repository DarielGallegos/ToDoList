import sqlite3
from src.backend.repositories.connect.repositoryDB import RepositoryDB
from src.backend.models.data.events import Events
class EventContract(RepositoryDB):
    __table__ = "eventos"
    __attributes__ = {
        "id": ["id","INTEGER PRIMARY KEY AUTOINCREMENT"],
        "titulo": ["titulo","TEXT NOT NULL"],
        "descripcion": ["descripcion","TEXT NOT NULL"],
        "ubicacion": ["ubicacion","TEXT NOT NULL"],
        "fecha_inicio": ["fecha_inicio","DATE NOT NULL"],
        "fecha_final": ["fecha_final","DATE NOT NULL"],
        "estado": ["estado","INTEGER NOT NULL"]
    }
    __relations__ = {
        "fk_estado": f"FOREIGN KEY({__attributes__['estado'][0]}) REFERENCES estados(id)"
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
                query += f"{self.__relations__[key]},"
            query = query[:-1]
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
        
    def insert(self, event:Events) -> dict:
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
                    query += f"'{getattr(event, key)}', "
            query = query[:-2]
            query += ")"
            cur.execute(query)
            self.conn.commit()
            cur.close()
            return {"status":True, "data":event }
        except sqlite3.Error as e:
            print(e)
            return {"status":False, "data":None }
    
    def update(self, event:Events) -> dict:
        try:
            cur = self.conn.cursor()
            query = f"UPDATE {self.__table__} SET "
            for key in self.__attributes__:
                query += f"{self.__attributes__[key][0]} = '{getattr(event, key)}', "
            query = query[:-2]
            query += f" WHERE id = {event.id}"
            cur.execute(query)
            self.conn.commit()
            cur.close()
            return {"status":True, "data":event }
        except sqlite3.Error as e:
            print(e)
            return {"status":False, "data":None }
    
    def delete(self, id:int) -> dict:
        try:
            cur = self.conn.cursor()
            query = f"DELETE FROM {self.__table__} WHERE id = {id}"
            cur.execute(query)
            self.conn.commit()
            cur.close()
            return {"status":True, "data":id }
        except sqlite3.Error as e:
            print(e)
            return {"status":False, "data":None }