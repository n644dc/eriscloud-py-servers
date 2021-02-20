import glob
import os
import sqlite3

class SqliteService:
    DB_FULL_PATH = None
    conn = None
    curs = None

    def __init__(self, db_full_path):
        self.DB_FULL_PATH = db_full_path
        self.createVerifyDbFile()

        self.conn = sqlite3.connect(self.DB_FULL_PATH)
        self.curs = self.conn.cursor()

    def createVerifyDbFile(self): 
        if not os.path.isfile(self.DB_FULL_PATH):
            print("Warning: DB does not exist, creating new.")
            with open(self.DB_FULL_PATH, "w"):
                pass
        else:
            print("Existing DB file found. Using that.")
            

    def createTable(self, tableName, columns):
        columnString = ""

        for col in columns:
            columnString += "{} {},".format(col[0],col[1])

        self.curs.execute('''CREATE TABLE stocks
                    (date text, trans text, symbol text, qty real, price real)''')
        self.commit()

    def insertToTable(self, table, values):
        valuesString = ", ".join(values)
        query = "INSERT INTO {} VALUES ({})".format(table, valuesString)
        print(query)
        #self.curs.execute(query)
        #self.commit()

    def commit(self):
        self.conn.commit()

    def closeConnection(self):
        self.conn.close()


