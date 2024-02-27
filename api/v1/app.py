#!/usr/bin/python3
"""Main module for the Flask web application."""
import os

from flask import Flask
from flask_cors import CORS

from api.v1.views import app_views
from models import storage

# Create a Flask app
web_app = Flask(__name__)
CORS(web_app, resources={r"/*": {"origins": "0.0.0.0"}})

# Register the blueprint for API routes
web_app.register_blueprint(app_views, url_prefix="/api/v1")


@web_app.teardown_appcontext
def close_db_session(app_context):
    """Close the database session after each request."""
    storage.close()


@web_app.errorhandler(404)
def handle_not_found(error):
    """Handle 404 errors by returning a JSON response."""
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    HOST = os.getenv('WEB_API_HOST', "0.0.0.0")
    PORT = int(os.getenv('WEB_API_PORT', 5000))
    web_app.run(host=HOST, port=PORT, threaded=True)
