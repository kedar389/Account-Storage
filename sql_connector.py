import sqlite3


class SqlConnector:
    def __init__(self, db_file):
        self.file = db_file
        self.connection = sqlite3.connect(self.file)
        self.cur = self.connection.cursor()

    def table_creator(self):
        sql_table = """CREATE TABLE IF NOT EXISTS accounts (
                        id integer PRIMARY KEY,
                        site text NOT NULL,
                        name text NOT NULL,
                        password text NOT NULL
                        );"""
        self.cur.execute(sql_table)

    def add_record(self, data):
        sql_query = """INSERT INTO accounts(id,site,name,password)
                        VALUES (?,?,?,?) """
        self.cur.execute(sql_query, data)

    def delete_record(self, input_id):
        sql_query = "DELETE FROM accounts WHERE id=?"
        self.cur.execute(sql_query, (input_id,))

    def get_all_records(self):
        sql = " SELECT * FROM accounts  "
        self.cur.execute(sql)

        return self.cur.fetchall()
