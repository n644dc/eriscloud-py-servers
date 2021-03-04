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

    # ###############################################
    def createVerifyDbFile(self): 
        if not os.path.isfile(self.DB_FULL_PATH):
            print("~*~*~*~*~ Warning: DB does not exist, creating new.")
            with open(self.DB_FULL_PATH, "w"):
                pass
        else:
            print("~*~*~*~*~ Existing DB file found. Using that.")
            
    # ###############################################
    def createTable(self, tableName, columns):
        if self.tableExists(tableName):
            return False, "table already exists"

        columnString = ""
        for col in columns:
            dataTypeKey = list(col)[0]
            columnString += "{} {}, ".format(col[dataTypeKey], dataTypeKey)
        columnString = columnString.strip().rstrip(',')
        query = "CREATE TABLE {} ({})".format(tableName, columnString)

        try:
            print("~*~*~*~*~ " + query)
            self.curs.execute(query)
            self.commit()
        except Exception as e:
            status = "Error: " + str(e)
            return False, status 

        return True, "Table created successfully."

    # ###############################################
    def insertToTable(self, tableName, values, keyColumnName=None):

        if keyColumnName is not None:
            recExists = self.recordExists(tableName, keyColumnName, values[0])
            if recExists:
                return False, "Record Already Exists."

        try:
            valuesString = ", ".join(values)
            query = "INSERT INTO {} VALUES ({})".format(tableName, valuesString)
            self.curs.execute(query)
            self.commit()
        except Exception as e:
            status = "ERROR: insertToTable: " + str(e)
            print(status)
            return False, status

        return True, "Successful Insert."

    # ###############################################
    def selectFromTable(self, tableName, selectFields=None, whereParams=None):
        resultArray = []
        query = ""
        status = "OK"
        if whereParams is None and selectFields is None:
            query = "SELECT * FROM {}".format(tableName)

        if whereParams and selectFields:
            query = "SELECT {} FROM {} WHERE {}".format(selectFields, tableName, whereParams)

        if whereParams and selectFields is None:
            query = "SELECT * FROM {} WHERE {}".format(tableName, whereParams)

        if selectFields and whereParams is None:
            query = "SELECT {} FROM {}".format(selectFields, tableName)

        try:
            print("~*~*~*~*~ " + query)
            self.curs.execute(query)
            resultArray = self.curs.fetchall()
        except Exception as e:
            status = "ERROR selectFromTable: " + str(e)
            print(status)

        return resultArray, status
    
    # ###############################################
    def recordExists(self, tableName, columnName, recordId):
        whereClause = columnName + " = " + recordId
        resultArray, status = self.selectFromTable(tableName, None, whereClause)
        if len(resultArray) > 1 and status is "OK":
            return True
        return False

    # ###############################################
    def tableExists(self, tableName):
        resultsArray, status = self.selectFromTable(tableName)
        if "no such table" in status and len(resultsArray) < 1:
            return False
        return True

    # ###############################################
    def commit(self):
        self.conn.commit()
    
    # ###############################################
    def closeConnection(self):
        self.conn.close()


