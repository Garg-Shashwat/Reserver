from flask import g
import sqlite3

from reserver.constants import DATABASE
from reserver import app


class Query:
    def __init__(self, table: str, fields: dict, columns: list = []) -> None:
        self.table = table
        self.fields = fields
        columns = list(map(columns, str.strip))
        self.select_columns = columns
        print(columns)

    def select_query():
        query = f"SELECT"


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


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()
