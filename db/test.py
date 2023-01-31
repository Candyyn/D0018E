from db.main import Database
import json

class Test:
    array = []

    def __init__(self, authToken):
        self.array = []
        database = Database().db
        cursor = database.cursor()
        cursor.execute("SELECT * FROM userTest")
        self.raw = cursor.fetchall()

        if(self.raw is not None) and (type(self.raw) is list):
            for i in self.raw:
                self.array.append(i)
        else:
            raise KeyError("User not found")
        pass
