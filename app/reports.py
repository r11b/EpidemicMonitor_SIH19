from bson.objectid import ObjectId
from bson.errors import InvalidId
from collections import defaultdict

from flask import Blueprint, render_template, redirect, url_for
from werkzeug.exceptions import abort

from app import mongo
from app.admin_auth import login_required

bp = Blueprint('reports', __name__, url_prefix='/reports')


@bp.route('/list')
@login_required
def list_():
    reports = mongo.db.reports.find()
    disease_wise_reports = defaultdict(list)

    for report in reports:
        disease_wise_reports[report['disease']].append(report['_id'])

    sorted_reports = sorted(disease_wise_reports.items(), key=lambda x: x[0])

    return render_template('reports/list_.html', reports=sorted_reports)


def get_report(id):
    try:
        report = mongo.db.reports.find_one({'_id': ObjectId(id)})
    except InvalidId:
        abort(404, 'Report with id {} doesn\'t exist in database.'.format(id))
    if report is None:
        abort(404, 'Report with id {} doesn\'t exist in database.'.format(id))

    return report


@bp.route('/<id>')
@login_required
def info(id):
    report = get_report(id)
    return render_template('reports/info.html', report=report)


@bp.route('/<id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_report(id)
    mongo.db.reports.delete_one({'_id': ObjectId(id)})

    return redirect(url_for('reports.list_'))
