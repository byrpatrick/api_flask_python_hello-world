from flask import (
    Blueprint
)

from api.authorization import authorization_guard, permissions, admin_messages_permissions

bp_name = 'api-messages'
bp_url_prefix = '/api/messages'
bp = Blueprint(bp_name, __name__, url_prefix=bp_url_prefix)


@bp.route("/public")
def public():
    return {
        "message": "The API doesn't require an access token to share this message."
    }


@bp.route("/protected")
@authorization_guard
def protected():
    return {
        "message": "The API successfully validated your access token."
    }


@bp.route("/admin")
@authorization_guard
@permissions([admin_messages_permissions.read])
def admin():
    return {
        "message": "The API successfully recognized you as an admin."
    }
