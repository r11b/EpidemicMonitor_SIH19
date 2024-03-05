from flask import render_template, session, redirect, url_for, g
from werkzeug.security import check_password_hash

from app import app, mongo
from app.forms import AdminLoginForm, AdminCreateForm


@app.route('/', methods=('GET', 'POST'))
def index():
    # if g.user is not None:
    #     form = AdminCreateForm()
    #
    # form = AdminLoginForm()
    # if form.validate_on_submit():
    #     username = form.username.data
    #     password = form.password.data
    #     error = None
    #
    #     user = mongo.db.admin.find_one({'username': username})
    #     if user is None:
    #         error = 'Incorrect username.'
    #     elif not check_password_hash(user['password'], password):
    #         error = 'Incorrect password.'
    #
    #     if error is None:
    #         session.clear()
    #         session['user_id'] = str(user['_id'])
    #
    #         return redirect(url_for('index'))
    #
    #     flash(error)

    return render_template('index.html')
