from flask import g
import sqlite3

from reserver.constants import DATABASE
from reserver import app


class Query:
    def __init__(self, table: str, fields: dict, columns: list = None) -> None:
        self.table = table
        self.fields = fields
        self.columns = ", ".join(list(map(str.strip, columns))) if columns else "*"

    def select_query(self, doReturn=False):
        query = f"SELECT {self.columns} FROM {self.table} WHERE {' = ? AND '.join(self.fields.keys())} = ?"
        if doReturn:
            return query, list(self.fields.values())
        else:
            return None

    def insert_query(self, doReturn=False):
        query = f"INSERT INTO {self.table} ({', '.join(self.fields.keys())}) VALUES ({', '.join(['?']*len(self.fields))})"
        if doReturn:
            return query, list(self.fields.values())
        else:
            return None

    def call_select_query(self, one=False):
        query, values = self.select_query(doReturn=True)
        return query_db(query, values, one)

    def call_insert_query(self):
        query, values = self.insert_query(doReturn=True)
        return query_db(query, values)


def init_db(init: bool = True):
    schema = "schema/init_schema.sql" if init else "schema/update_schema.sql"
    with app.app_context():
        db = get_db()
        with app.open_resource(schema, mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def query_db(query, args=(), one=False, type="SELECT"):
    db = get_db()
    cur = db.execute(query, args)
    if type == "SELECT":
        rv = cur.fetchall()
        return_val = (rv[0] if rv else None) if one else rv
    elif type == "INSERT":
        db.commit()
        return_val = cur.rowcount
    db.close()
    return return_val


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()
