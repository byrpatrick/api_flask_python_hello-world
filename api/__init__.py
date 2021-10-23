import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_talisman import Talisman
from werkzeug import exceptions

from api import messages


def create_app():
    client_origin_url = os.environ.get("CLIENT_ORIGIN_URL")

    app = Flask(__name__, instance_relative_config=True)
    Talisman(app)
    CORS(
        app,
        resources={r"/api/*": {"origins": client_origin_url}}
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(messages.bp)

    @app.errorhandler(exceptions.NotFound)
    def _handle_not_found_error(ex):
        if request.path.startswith('/api/'):
            return {"message": "Not Found"}, ex.code
        else:
            return ex

    @app.errorhandler(exceptions.InternalServerError)
    def _handle_internal_server_error(ex):
        if request.path.startswith('/api/'):
            return jsonify(message=str(ex)), ex.code
        else:
            return ex

    return app
