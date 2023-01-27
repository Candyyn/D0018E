from db.main import Database


class User:
    id = None
    username = None
    email = None
    create_time = None
    raw = None

    def __init__(self, authToken):
        database = Database().db
        cursor = database.cursor()
        cursor.execute("SELECT * FROM userTest")
        self.raw = cursor.fetchall()

        if type(self.raw) is not list and self.raw is not None:
            self.id = self.raw[0]
            self.username = self.raw[1]
            self.email = self.raw[2]
            self.create_time = self.raw[3]
        else:
            raise KeyError("User not found")
        pass
