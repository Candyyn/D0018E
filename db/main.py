import mysql.connector


class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="utbweb.its.ltu.se",
            user="20001105",
            password="20001105",
            database="db20001105"
        )
