import mysql.connector


class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="208.87.129.160",
            user="emil",
            password="QJYcDoO8DKoNIZodmBS1Jw",
            database="db20001105"
        )
