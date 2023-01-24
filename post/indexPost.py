from db.main import Database

class PostClass:
    def __init__(self):
        pass

    def exec(self, route_args):
        database = Database()
        mycursor = database.db.cursor();
        mycursor.execute("SHOW DATABASES;")
        for x in mycursor:
            print(x)

        return "{'test': 123}"
