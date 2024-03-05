import re

from bson.objectid import ObjectId
from bson.errors import InvalidId

from flask import Blueprint, render_template, redirect, url_for
from werkzeug.exceptions import abort

from app import mongo
from app.admin_auth import login_required
from app.forms import DiseaseAddForm, DiseaseEditForm, DiseaseSearchForm

bp = Blueprint('diseases', __name__, url_prefix='/diseases')


@bp.route('/list', methods=('GET', 'POST'))
def list_():
    form = DiseaseSearchForm()
    if form.validate_on_submit():
        query = form.search.data
        diseases = mongo.db.diseases.find({'name': re.compile(query, re.IGNORECASE)})
        sorted_diseases = sorted(list(diseases), key=lambda d: d['name'])

        return render_template('diseases/list_.html', diseases=sorted_diseases, form=form)

    diseases = mongo.db.diseases.find()
    sorted_diseases = sorted(list(diseases), key=lambda d: d['name'])

    return render_template('diseases/list_.html', diseases=sorted_diseases, form=form)


@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    form = DiseaseAddForm()
    if form.validate_on_submit():
        disease = {
            'name': form.name.data.strip(),
            'desc': form.desc.data.strip(),
            'type': form.type_.data.strip(),
            'symptoms': [s.strip() for s in form.symptoms.data.split('\n')],
            'diagnosis': [s.strip() for s in form.diagnosis.data.split('\n')],
            'complications': [s.strip() for s in form.complications.data.split('\n')],
            'transmissions': [s.strip() for s in form.transmissions.data.split('\n')],
            'causes': [s.strip() for s in form.causes.data.split('\n')],
            'deaths': form.deaths.data.strip(),
            'onset': form.onset.data.strip(),
            'medications': [s.strip() for s in form.medications.data.split('\n')],
            'links': [s.strip() for s in form.links.data.split('\n')]
        }
        mongo.db.diseases.insert_one(disease)

        return redirect(url_for('diseases.list_'))

    return render_template('diseases/add.html', form=form)


def get_disease(id):
    try:
        disease = mongo.db.diseases.find_one({'_id': ObjectId(id)})
    except InvalidId:
        abort(404, 'Disease with id {} doesn\'t exist in database.'.format(id))
    if disease is None:
        abort(404, 'Disease with id {} doesn\'t exist in database.'.format(id))

    return disease


@bp.route('/<id>')
def info(id):
    disease = get_disease(id)
    return render_template('diseases/info.html', disease=disease)


@bp.route('/<id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    disease = get_disease(id)
    form = DiseaseEditForm()

    if form.validate_on_submit():
        mongo.db.diseases.update_one(
            {'_id': ObjectId(disease['_id'])},
            {'$set': {
                'name': form.name.data.strip(),
                'desc': form.desc.data.strip(),
                'type': form.type_.data.strip(),
                'symptoms': [s.strip() for s in form.symptoms.data.split('\n')],
                'diagnosis': [s.strip() for s in form.diagnosis.data.split('\n')],
                'complications': [s.strip() for s in form.complications.data.split('\n')],
                'transmissions': [s.strip() for s in form.transmissions.data.split('\n')],
                'causes': [s.strip() for s in form.causes.data.split('\n')],
                'deaths': form.deaths.data.strip(),
                'onset': form.onset.data.strip(),
                'medications': [s.strip() for s in form.medications.data.split('\n')],
                'links': [s.strip() for s in form.links.data.split('\n')]
            }}
        )

        return redirect(url_for('diseases.info', id=id))

    return render_template('diseases/edit.html', form=form, disease=disease)


@bp.route('/<id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_disease(id)
    mongo.db.diseases.delete_one({'_id': ObjectId(id)})

    return redirect(url_for('diseases.list_'))
