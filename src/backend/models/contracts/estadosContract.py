import sqlite3
from src.backend.repositories.connect.repositoryDB import RepositoryDB
class EstadosContract(RepositoryDB):
    __table__ = "estados"
    __attributes__ = {
        "id": ["id","INTEGER PRIMARY KEY AUTOINCREMENT"],
        "nombre": ["nombre","TEXT NOT NULL"]
    }

    def __init__(self):
        super().__init__()

    def createTable(self):
        try:
            cur = self.getConnect().cursor()
            query = f"CREATE TABLE IF NOT EXISTS {self.__table__} ("
            for key in self.__attributes__:
                query += f"{self.__attributes__[key][0]} {self.__attributes__[key][1]}, "
            query = query[:-2]
            query += ")"
            cur.execute(query)
            self.conn.commit()
            cur.close()
        except sqlite3.Error as e:
            print(e)