from bson.objectid import ObjectId
from bson.errors import InvalidId

from flask import Blueprint, render_template, redirect, url_for

from app import mongo
from app.admin_auth import login_required

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/list')
@login_required
def list_():
    users = mongo.db.users.find()
    sorted_users = sorted(list(users), key=lambda d: d['name'])
    return render_template('users/list_.html', users=sorted_users)


def get_user(id):
    try:
        user = mongo.db.users.find_one({'_id': ObjectId(id)})
    except InvalidId:
        abort(404, 'User with id {} doesn\'t exist in database.'.format(id))
    if user is None:
        abort(404, 'User with id {} doesn\'t exist in database.'.format(id))

    return user


@bp.route('/<id>')
@login_required
def info(id):
    user = get_user(id)
    return render_template('users/info.html', user=user)


@bp.route('/<id>/verify', methods=('POST',))
@login_required
def verify(id):
    get_user(id)
    mongo.db.users.update_one(
        {'_id': ObjectId(id)},
        {'$set': {
            'verified': 'true'
        }}
    )

    return redirect(url_for('users.info', id=id))


@bp.route('/<id>/unsuspend', methods=('POST',))
@login_required
def unsuspend(id):
    get_user(id)
    mongo.db.users.update_one(
        {'_id': ObjectId(id)},
        {'$set': {
            'suspended': 'false'
        }}
    )

    return redirect(url_for('users.info', id=id))


@bp.route('/<id>/suspend', methods=('POST',))
@login_required
def suspend(id):
    get_user(id)
    mongo.db.users.update_one(
        {'_id': ObjectId(id)},
        {'$set': {
            'suspended': 'true'
        }}
    )

    return redirect(url_for('users.info', id=id))
