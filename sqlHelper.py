import sqlite3


class sqlHelper:
    def __init__(self, db, table):
        self.table = table
        self.con = sqlite3.connect(db, check_same_thread=False)
        self.cur = self.con.cursor()

    def getUserByTelegramID(self, telegramID):
        self.cur.execute(f"SELECT * FROM {self.table} WHERE telegramID={telegramID};")
        one_result = self.cur.fetchone()
        return one_result
