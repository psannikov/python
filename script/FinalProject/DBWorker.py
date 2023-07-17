import sqlite3


class DBWorker:
    def __init__(self, db_name):
        self.db_name = db_name

    def insert_df_to_db(self, table_name, data_frame):
        connection = sqlite3.connect(self.db_name)
        data_frame.to_sql(table_name, connection, if_exists='replace', index=False)
        connection.close()
