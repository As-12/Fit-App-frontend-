from sqlalchemy.exc import IntegrityError

from main import api, logger

from flask_restx import Resource, abort

from flask import request

from models.user import user_model, user_list_model, user_patch_model
from database.user import User

user_ns = api.namespace('users', description='User operations')


@user_ns.route('/')
class UserList(Resource):
    '''Shows a list of all users'''

    @user_ns.marshal_list_with(user_list_model)
    def get(self):
        '''Get a list of users'''

        logger.info(f"GET request to user list from {request.remote_addr}")
        users = User.query.all()
        response = {
            "users": users,
            "count": len(users)
        }

        return response

    @user_ns.marshal_with(user_model)
    @user_ns.expect(user_model)
    def post(self):
        '''Create a new user'''

        logger.info(f"POST request to create user {api.payload['id']} from {request.remote_addr}")
        try:
            user = User(**api.payload)
            user.insert()
            code = 201
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
    '''Shows a list of all users'''

    @user_ns.marshal_with(user_model)
    def get(self, user_id):
        '''Get questions by Id'''
        logger.info(f"GET request to user {user_id} from {request.remote_addr}")
        user = User.query.get(user_id)
        if user is None:
            logger.debug(f"GET error {user_id} does not exist ")
            abort(404, f"User {user_id} does not exist.")
        return user

    def delete(self, user_id):
        '''Delete existing user'''

        logger.info(f"DELETE request to user {user_id} from {request.remote_addr}")
        try:
            user = User.query.get(user_id)
            if user is None:
                logger.debug(f"DELETE error {user_id} does not exist ")
                code = 404
                message = f"User {user_id} does not exist."
            else:
                user.delete()
                code = 204
        except Exception as e:
            logger.debug(f"DELETE error {user_id} Exception: {e} ")
            code = 500
            message = f"Server encountered issue deleting user {user_id}"

        if code != 204:
            abort(code, message)

        return '', 204

    @user_ns.marshal_with(user_model)
    @user_ns.expect(user_patch_model)
    def patch(self, user_id):
        '''Update existing user'''

        logger.info(f"PATCH request to modify user {user_id} from {request.remote_addr}")

        try:
            # @TODO: Verify if the payload user_id is the same as token_id
            user = User.query.get(user_id)
            if user is None:
                logger.debug(f"PATCH error {user_id} does not exist ")
                code = 404
                message = f"User {user_id} does not exist."
            else:
                user = User(**api.payload)
                user.update()
                code = 204
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

