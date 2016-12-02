import sqlite3

class Database(object):
    """Interface to a local database that stores data for the website.
    """
    def __init__(self, dbname):
        self.dbname = dbname


    @property
    def conn(self):
        return sqlite3.connect(self.dbname)


    @property
    def cursor(self):
        return self.conn.cursor()


    def select(self, table, fields, condition=None):
        cur = self.cursor

        if condition is not None:
            cur.execute("SELECT {} FROM {} WHERE {}".format(fields, table,
                                                                    condition))
        else:
            cur.execute("SELECT {} FROM {}".format(fields, table))

        return cur.fetchall()


    def create_table(self, table, cols):
        conn = self.conn
        cur = conn.cursor()

        query = "CREATE TABLE {}({})".format(table, cols)
        cur.execute(query)
        conn.commit()


    def insert(self, table, columns, values, params):
        conn = self.conn
        cur = conn.cursor()

        query = "INSERT INTO {}({}) VALUES ({})".format(table, columns, values)
        cur.execute(query, params)
        conn.commit()


    def delete(self, table, condition):
        conn = self.conn
        cur = conn.cursor()

        query = "DELETE FROM {} WHERE {}".format(table, condition)
        cur.execute(query)
        conn.commit()
