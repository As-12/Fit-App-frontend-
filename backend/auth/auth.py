import json
from configparser import ConfigParser

from flask import request, _request_ctx_stack, abort, jsonify
from functools import wraps
from jose import jwt
from six.moves.urllib.request import urlopen

configParser = ConfigParser()
configFilePath = r'conf/auth.conf'
configParser.read(configFilePath)


AUTH0_DOMAIN = configParser.get('Auth', 'AUTH0_DOMAIN')
ALGORITHMS = [configParser.get('Auth',  'AUTH0_ALGORITHM')]
API_AUDIENCE = configParser.get('Auth', 'AUTH0_API_AUDIENCE')

"""
Authentication and Authorization

The code is based from Auth0 Python SDK
https://auth0.com/docs/quickstart/backend/python/01-authorization

"""


# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)
    token = request.headers['Authorization'].split(" ")
    if len(token) != 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    if token[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    return token[1]



def verify_decode_jwt(token):
    """Determines if the Access Token is valid
        """
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)

def check_permissions(permission, payload, user_id):
    """ Authorize scope Permission """
    try:
        # Validate permission scope
        if permission != '' and permission not in payload['permissions']:
            raise AuthError({
                'code': 'Forbidden',
                'description': 'Insufficient permission to perform the request.'
            }, 403)
        # Validate if user is accesssing their own resource
        if user_id != '' and payload['sub'] != user_id:
            raise AuthError({
                'code': 'Forbidden',
                'description': 'You do not have permission to perform this task on another user resource.'
            }, 403)

    except AuthError:
        raise
    except Exception as e:
        raise AuthError({
            'code': 'invalid_key',
            'description': 'authorization token does not contain permission. Ensure that RBAC is enabled and the user '
                           'has an appropriate role assigned '
        }, 401)


def requires_auth(permission=''):
    """Authentication and Authorization Decorator
    """

    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload, '')
            except AuthError as e:
                abort(e.status_code, e.error)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator


def requires_auth_with_same_user(permission=''):
    """Authentication and Authorization Decorator
       Requires the user to make claim on its own resource
    """

    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(user_id, *args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload, user_id)
            except AuthError as e:
                abort(e.status_code, e.error)
            return f(user_id, payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator

