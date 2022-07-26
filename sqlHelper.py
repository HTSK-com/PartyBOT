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

    def editDataBase(self, telegramID, param, value):  # Эту функцию необходимо проверить
        # print(f"UPDATE INTO {self.table} ({param}) VALUES({value}) WHERE telegramID={telegramID};")
        self.cur.execute(f"UPDATE {self.table} SET {param} = {value} WHERE telegramID={telegramID};")
        self.con.commit()

    def newRecord(self, listOfNames, listOfValues):
        self.cur.execute(f"INSERT INTO {self.table} ({', '.join(listOfNames)}) VALUES ({', '.join(listOfValues)});")
        self.con.commit()