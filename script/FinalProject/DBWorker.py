import sqlite3


class DBWorker:
    def __init__(self, dbName):
        self.dbName = dbName

    def insertDfToDB(self, tableName, dataFrame):
        connection = sqlite3.connect(self.dbName)
        dataFrame.to_sql(tableName, connection, if_exists='replace', index=False)
        connection.close()
