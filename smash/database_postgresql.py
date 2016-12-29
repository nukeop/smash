import os
import psycopg2
import urlparse

class DatabasePostgreSQL(object):
    """Interface to the heroku PostgreSQL database plugin.
    """
    def __init__(self):
        urlparse.uses_netloc.append("postgres")
        self.url = urlparse.urlparse(os.environ["DATABASE_URL"])


    @property
    def conn(self):
        return psycopg2.connect(
            database=self.url.path[1:],
            user=self.url.username,
            password=self.url.password,
            host=self.url.hostname,
            port=self.url.port
        )


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
        return cur


    def delete(self, table, condition):
        conn = self.conn
        cur = conn.cursor()

        query = "DELETE FROM {} WHERE {}".format(table, condition)
        cur.execute(query)
        conn.commit()
