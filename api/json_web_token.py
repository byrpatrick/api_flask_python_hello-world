import os
from http import HTTPStatus
from urllib.error import HTTPError

import jwt

from api.utils import json_abort


class JsonWebToken:
    """Perform JSON Web Token (JWT) validation using PyJWT"""

    def __init__(self, token):
        self.token = token
        auth0_domain = os.environ.get("AUTH0_DOMAIN")
        self.auth0_issuer_url = f'https://{auth0_domain}/'
        self.jwks_uri = f'{self.auth0_issuer_url}.well-known/jwks.json'
        self.auth0_audience = os.environ.get("AUTH0_AUDIENCE")
        self.algorithm = 'RS256'

    def validate(self):
        try:
            jwks_client = jwt.PyJWKClient(self.jwks_uri)
            jwt_signing_key = jwks_client.get_signing_key_from_jwt(
                self.token
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
                self.token,
                jwt_signing_key,
                algorithms=self.algorithm,
                audience=self.auth0_audience,
                issuer=self.auth0_issuer_url,
            )
        except Exception as error:
            json_abort(HTTPStatus.UNAUTHORIZED, {
                "error": "invalid_token",
                "error_description": error.__str__(),
                "message": "Unauthorized."
            })
            return

        return payload
