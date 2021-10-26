import os
from http import HTTPStatus
from urllib.error import HTTPError

import jwt

from api.utils import json_abort

_auth0_domain = os.environ.get("AUTH0_DOMAIN")
_auth0_issuer_url = f'https://{_auth0_domain}/'
_jwks_uri = f'{_auth0_issuer_url}.well-known/jwks.json'
_auth0_audience = os.environ.get("AUTH0_AUDIENCE")
_algorithm = 'RS256'

_jwks_client = jwt.PyJWKClient(_jwks_uri)


def validate_jwt(token):
    try:
        jwt_signing_key = _jwks_client.get_signing_key_from_jwt(
            token
        ).key
    except (jwt.exceptions.PyJWKClientError, HTTPError) as error:
        json_abort(HTTPStatus.UNAUTHORIZED, {
            "error": "signing_key_unavailable",
            "error_description": error.__str__(),
            "message": "Can't get signing key.."
        })
        return

    except jwt.exceptions.DecodeError as error:
        json_abort(HTTPStatus.UNAUTHORIZED, {
            "error": "invalid_token",
            "error_description": error.__str__(),
            "message": "Unauthorized."
        })
        return

    try:
        payload = jwt.decode(
            token,
            jwt_signing_key,
            algorithms=_algorithm,
            audience=_auth0_audience,
            issuer=_auth0_issuer_url,
        )
    except Exception as error:
        json_abort(HTTPStatus.UNAUTHORIZED, {
            "error": "invalid_token",
            "error_description": error.__str__(),
            "message": "Unauthorized."
        })
        return

    return payload
