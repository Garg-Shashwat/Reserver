from flask import request, session, redirect, render_template, url_for

from reserver import app
from reserver.db_methods import query_db

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = query_db('SELECT * FROM users WHERE username = ? AND password = ? AND is_admin = 0', [username, password], one=True)
        admin = query_db('SELECT * FROM users WHERE username = ? AND password = ? AND is_admin = 1', [username, password], one=True)
        if user:
            session['username'] = user['username']
            session['is_admin'] = False
            return redirect(url_for('home'))
        elif admin:
            session['username'] = admin['username']
            session['is_admin'] = True
            return redirect(url_for('admin_home'))
        else:
            return render_template('login.html', error=True)
    else:
        return render_template('login.html', error=False)
