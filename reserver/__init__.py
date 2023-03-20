from flask import Flask

app = Flask(__name__)
app.secret_key = 'Noman'

import reserver.db_methods
import reserver.login
import reserver.home

if __name__ == '__main__':
    app.run()
