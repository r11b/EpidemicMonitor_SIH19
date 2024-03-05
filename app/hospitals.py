import re

from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.exceptions import abort

from app import mongo
from app.admin_auth import login_required
from app.forms import HospitalAddForm, HospitalEditForm, HospitalSearchForm

bp = Blueprint('hospitals', __name__, url_prefix='/hospitals')


@bp.route('/list', methods=('GET', 'POST'))
def list_():
    form = HospitalSearchForm()
    if form.validate_on_submit():
        query = form.search.data
        hospitals = mongo.db.hospitals.find({'name': re.compile(query, re.IGNORECASE)})
        sorted_hospitals = sorted(list(hospitals), key=lambda d: d['name'])

        return render_template('hospitals/list_.html', hospitals=sorted_hospitals, form=form)

    hospitals = mongo.db.hospitals.find()
    sorted_hospitals = sorted(list(hospitals), key=lambda d: d['name'])

    return render_template('hospitals/list_.html', hospitals=sorted_hospitals, form=form)



@bp.route('/add', methods=('POST', 'GET'))
@login_required
def add():
    form = HospitalAddForm()
    if form.validate_on_submit():
        hospital = {
            'id': form.id.data.strip(),
            'name': form.name.data.strip(),
            'location': {
                'latitude': form.latitude.data.strip(),
                'longitude': form.longitude.data.strip(),
                'address': form.address.data.strip()
            },
            'contact': [s.strip() for s in form.contact.data.split('\n')],
            'website': form.website.data.strip()
        }
        mongo.db.hospitals.insert_one(hospital)

        return redirect(url_for('hospitals.list_'))

    return render_template('hospitals/add.html', form=form)


def get_hospital(id):
    try:
        hospital = mongo.db.hospitals.find_one({'_id': ObjectId(id)})
    except InvalidId:
        abort(404, 'Hospital with id {} doesn\'t exist in database.'.format(id))
    if hospital is None:
        abort(404, 'Hospital with id {} doesn\'t exist in database.'.format(id))

    return hospital


@bp.route('/<id>')
def info(id):
    hospital = get_hospital(id)
    return render_template('hospitals/info.html', hospital=hospital)


@bp.route('/<id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    hospital = get_hospital(id)
    form = HospitalEditForm()

    if form.validate_on_submit():
        mongo.db.hospitals.update_one(
            {'_id': ObjectId(hospital['_id'])},
            {'$set': {
                'id': form.id.data.strip(),
                'name': form.name.data.strip(),
                'location': {
                    'latitude': form.latitude.data.strip(),
                    'longitude': form.longitude.data.strip(),
                    'address': form.address.data.strip()
                },
                'contact': [s.strip() for s in form.contact.data.split('\n')],
                'website': form.website.data.strip()
            }}
        )

        return redirect(url_for('hospitals.info', id=id))

    return render_template('hospitals/edit.html', form=form, hospital=hospital)


@bp.route('/<id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_hospital(id)
    mongo.db.hospitals.delete_one({'_id': ObjectId(id)})

    return redirect(url_for('hospitals.list_'))
