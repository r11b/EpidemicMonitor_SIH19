from collections import defaultdict

from flask import Blueprint, render_template

from app import mongo

bp = Blueprint('maps', __name__, url_prefix='/maps')


@bp.route('/projections')
def projections():
    projections = mongo.db.projections.find()
    disease_data = defaultdict(dict)
    for doc in projections:
        disease_data[doc['disease']]['ver{}'.format(doc['ver'])] = {
            'infected': doc['points'],
            'cured': doc['cpoints'],
            'dead': doc['dpoints']
        }


    pune = {'lat': 18.5204, 'lng': 73.8567}
    india = {'lat': 20.5937, 'lng': 78.9629}

    kwargs = {
        'map_center': india,
        'zoom': 5,
        'diseases': list(disease_data.keys()),
        'disease_data': disease_data,
        'weeks': list(range(5)),
        'radius': 15,
        'opacity': 0.75,
    }


    return render_template('maps/projections.html', **kwargs)
