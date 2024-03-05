import functools
import sys
from bson.objectid import ObjectId

from flask import Blueprint, g, redirect, render_template, session, url_for, flash, request
from werkzeug.security import check_password_hash, generate_password_hash

from app import mongo
from app.forms import AdminLoginForm, AdminCreateForm

bp = Blueprint('admin', __name__, url_prefix='/admin')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('admin.login', next=request.endpoint))

        return view(**kwargs)

    return wrapped_view


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        error = None

        user = mongo.db.admin.find_one({'username': username})
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = str(user['_id'])

            next_page = request.args.get('next')
            try:
                next_url = url_for(next_page)
            except:
                next_url = url_for('index')

            return redirect(next_url)

        flash(error)

    return render_template('admin/login.html', form=form)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = AdminCreateForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if mongo.db.admin.find_one({'username': username}) is not None:
            flash('{} is already a registered admin.'.format(username))

        mongo.db.admin.insert_one({
            'username': username,
            'password': generate_password_hash(password)
        })

        return redirect(url_for('index'))

    return render_template('admin/create.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = mongo.db.admin.find_one({'_id': ObjectId(user_id)})


@bp.route('/logout')
def logout():
    session.clear()
    next_page = request.args.get('next')
    try:
        next_url = url_for(next_page)
    except:
        next_url = url_for('index')

    return redirect(next_url)
