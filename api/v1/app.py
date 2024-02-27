#!/usr/bin/python3
'''
Creating Flask myapp & register blueprint app_views to Flask instance myapp
'''

from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

myapp = Flask(__name__)

# enable CORS and allow for origins:
CORS(myapp, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})

myapp.register_blueprint(app_views)
myapp.url_map.strict_slashes = False


@myapp.teardown_appcontext
def teardown_engin(exception):
    '''
    removing current SQLAlchemy session obj after each request
    '''
    storage.close()


# error handlers for expected myapp behavior
@myapp.errorhandler(404)
def not_found(error):
    '''
    returning error msg `Not Found`
    '''
    response = {'error': 'Not found'}
    return jsonify(response), 404


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    myapp.run(host=HOST, port=PORT, threaded=True)