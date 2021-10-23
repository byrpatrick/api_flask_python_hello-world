from flask import (
    Blueprint
)

bp_name = 'api-messages'
bp_url_prefix = '/api/messages'
bp = Blueprint(bp_name, __name__, url_prefix=bp_url_prefix)


@bp.route("/public")
def public():
    return {
        "message": "The API doesn't require an access token to share this message."
    }


@bp.route("/protected")
def protected():
    return {
        "message": "The API successfully validated your access token."
    }


@bp.route("/admin")
def admin():
    return {
        "message": "The API successfully recognized you as an admin."
    }
