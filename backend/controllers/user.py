from sqlalchemy.exc import IntegrityError

from auth.auth import requires_auth, requires_auth_with_same_user
from main import api, logger

from flask_restx import Resource, abort

from flask import request

from models.user import user_model, user_list_model, user_patch_model
from database.user import User
from database.progress import Progress
user_ns = api.namespace('users', description='User operations')


@user_ns.route('/')
class UserList(Resource):

    @user_ns.marshal_list_with(user_list_model)
    @requires_auth('read:user')
    def get(self, payload):
        """Get a list of all users. This endpoint requires read:user permission"""

        logger.info(f"GET request to user list from {request.remote_addr}")
        users = User.query.all()
        response = {
            "users": users,
            "count": len(users)
        }
        return response

    @user_ns.marshal_with(user_model, code=201)
    @user_ns.expect(user_model)
    @requires_auth()
    def post(self, payload):
        """Create a new user. Only authenticating user can post
           User ID is defined by the verified subject in the access token
        """
        logger.info(f"POST request to create user {payload['sub']} from {request.remote_addr}")
        try:
            user = User(**api.payload)
            user.id = payload['sub']
            api.payload['id'] = payload['sub']
            user.insert()
            code = 201
        except ValueError as e:
            code = 422
            message = str(e)
        except IntegrityError:
            code = 422
            message = "Cannot add to existing user. Use Patch request instead"
        except Exception as e:
            logger.debug(e)
            code = 400
            message = "The request data format is not valid"

        if code != 201:
            abort(code, message)

        return api.payload, 201


@user_ns.route('/<user_id>')
class Users(Resource):

    @user_ns.marshal_with(user_model)
    @requires_auth_with_same_user()
    def get(self, payload, user_id):
        """Obtain user information. Only authenticated user can access their own resource"""
        logger.info(f"GET request to user {user_id} from {request.remote_addr}")
        user = User.query.get(user_id)
        if user is None:
            logger.debug(f"GET error {user_id} does not exist ")
            abort(404, f"User {user_id} does not exist.")
        return user

    @requires_auth('delete:user')
    @user_ns.response(204, 'User deleted successfully')
    def delete(self, payload, user_id):
        """Delete existing user. Require delete:user permission
           This will also delete associated progress for this user
        """

        logger.info(f"DELETE request to user {user_id} from {request.remote_addr}")
        try:
            user = User.query.get(user_id)
            if user is None:
                logger.debug(f"DELETE error {user_id} does not exist ")
                code = 404
                message = f"User {user_id} does not exist."
            else:
                associated_progress = Progress.query.filter(Progress.user_id == user_id).all()
                if associated_progress is not None:
                    logger.debug(f"DELETE: deleting all progress related to {user_id}")
                    for progress in associated_progress:
                        progress.delete()
                user.delete()
                code = 204
        except Exception as e:
            logger.debug(f"DELETE error {user_id} Exception: {e} ")
            code = 500
            message = f"Server encountered issue deleting user {user_id}"

        if code != 204:
            abort(code, message)

        return '', 204

    @user_ns.expect(user_patch_model)
    @user_ns.response(204, 'User modified successfully')
    @requires_auth_with_same_user()
    def patch(self, payload, user_id):
        """ Update user. Authenticated user can only access their own resource """

        logger.info(f"PATCH request to modify user {user_id} from {request.remote_addr}")
        try:
            user = User.query.get(user_id)
            if user is None:
                logger.debug(f"PATCH error {user_id} does not exist ")
                code = 404
                message = f"User {user_id} does not exist."
            else:
                user.update(api.payload)
                code = 204
        except ValueError as e:
            message = str(e)
            code = 422
        except IntegrityError:
            code = 422
            message = "Cannot patch existing user. Use Patch request instead"
        except Exception as e:
            logger.debug(e)
            code = 400
            message = "The request data format is not valid"

        if code != 204:
            abort(code, message)

        logger.debug(f"Modifying {user_id} is successful requested from {request.remote_addr}")

        return '', 204
