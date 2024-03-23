import sqlite3 as sq
import os
import time


# Создать таблицу "Instruction" с полями: instruction


class DataBase:
    def __init__(self, patch: str):
        self._patch = patch

    def create_table(self):
        self.get_cursor.execute("""CREATE TABLE IF NOT EXISTS Instruction (
                                           id INTEGER PRIMARY KEY, 
                                           description TEXT NOT NULL
                                           )""")

        # Список таблиц для создания
        tables = ['RussianCredentials', 'UmoneyCredentials', 'ForeignCredentials', 'CryptoCredentials']

        # Цикл для создания таблиц
        for table in tables:
            self.get_cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table} (
                                               id INTEGER PRIMARY KEY,
                                               number TEXT NOT NULL
                                               )""")

        return 1

    def drop_table(self):
        self.get_cursor.execute("DROP TABLE IF EXISTS Instruction")
        self.create_table()

    def edit_instruction(self, text):
        rows = self.get_cursor.execute("SELECT * FROM Instruction").fetchall()

        if len(rows) == 0:
            self.get_cursor.execute(f"INSERT INTO Instruction (description) VALUES (?)", (text, )).connection.commit()
        else:
            self.get_cursor.execute('UPDATE Instruction SET description = ? WHERE rowid = 1', (text,)).connection.commit()

    def add_credentials(self, table_name, card_number):
        rows = self.get_cursor.execute(f"SELECT * FROM {table_name}").fetchall()
        for (id, number) in rows:
            if number == card_number:
                return 1

        self.get_cursor.execute(f"INSERT INTO {table_name} (number) VALUES (?)", (card_number, )).connection.commit()

        return 0

    def delete_credentials(self, table_name):
        self.get_cursor.execute(f"DELETE FROM {table_name}").connection.commit()

    def get_info(self):
        result = {
            'instruction': self.get_cursor.execute("SELECT * FROM Instruction").fetchall(),
            'russian_cards': self.get_cursor.execute("SELECT * FROM RussianCredentials").fetchall(),
            'foreign_cards': self.get_cursor.execute("SELECT * FROM ForeignCredentials").fetchall(),
            'umoney': self.get_cursor.execute("SELECT * FROM UmoneyCredentials").fetchall(),
            'crypto': self.get_cursor.execute("SELECT * FROM CryptoCredentials").fetchall()
        }

        return result

    @property
    def get_cursor(self):
        with sq.connect(self._patch) as con:
            return con.cursor()

    def get_russian_credentials(self):
        return self.get_cursor.execute("SELECT * FROM RussianCredentials").fetchall()

    def get_foreign_credentials(self):
        return self.get_cursor.execute("SELECT * FROM ForeignCredentials").fetchall()

    def get_umoney_credentials(self):
        return self.get_cursor.execute("SELECT * FROM UmoneyCredentials").fetchall()

    def get_crypto_credentials(self):
        return self.get_cursor.execute("SELECT * FROM CryptoCredentials").fetchall()

