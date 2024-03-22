import sqlite3 as sq
import os
import time


# Создать таблицу "Instruction" с полями: instruction


class DataBase:
    def __init__(self, patch: str):
        self._patch = patch

    def create_table(self):
        self.get_cursor.execute("""CREATE TABLE IF NOT EXISTS Instruction (
                                   description TEXT NOT NULL
                                   )""")
        return 1

    def drop_table(self):
        self.get_cursor.execute("DROP TABLE IF EXISTS Instruction")
        self.create_table()

    def add_event(self, event_name, event_description, event_datee):
        self.get_cursor.execute('INSERT INTO Events (name, description, datee) VALUES (?, ?, ?)', (event_name, event_description, event_datee)).connection.commit()

    @property
    def get_cursor(self):
        with sq.connect(self._patch) as con:
            return con.cursor()


db = DataBase('data/Instruction.db')
db.create_table()
