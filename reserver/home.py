from flask import session, redirect, render_template, url_for

from reserver import app

@app.route('/')
def home():
    if 'username' in session:
        if session['is_admin']:
            return redirect(url_for('admin_home'))
        else:
            return render_template('user_home.html', username=session['username'])
    else:
        return redirect(url_for('login'))