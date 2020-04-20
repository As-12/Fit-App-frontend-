from datetime import datetime

from sqlalchemy.exc import IntegrityError

from auth.auth import requires_auth_with_same_user, requires_auth
from main import api, logger

from flask_restx import Resource, abort

from flask import request

from models.progress import progress_model, progress_list_model, all_progress_model
from database.progress import Progress, valid_emotion_value
from database.user import User

progress_ns = api.namespace('progress', description='Progress operations')


class IllegalArgumentError(ValueError):
    pass


@progress_ns.route('/')
class ProgressList(Resource):

    @progress_ns.marshal_list_with(all_progress_model)
    @requires_auth('read:progress')
    def get(self, payload):
        """Get a list of every user's progress. Requires read:progress permission"""

        logger.info(f"GET request to all progress list")

        progress_list = Progress.query.all()
        response = {
            "progresses": progress_list,
            "count": len(progress_list)
        }
        return response


@progress_ns.route('/<user_id>')
class Progresses(Resource):

    @progress_ns.marshal_list_with(progress_list_model)
    @requires_auth_with_same_user()
    def get(self, payload, user_id):
        """Get a list of user's progress. Only authenticated user can access their own resource"""

        logger.info(f"GET request to progress list of {user_id} from {request.remote_addr}")

        user = User.query.get(user_id)
        if user is None:
            code = 404
            message = f"Cannot track progress for {user_id}. User does not exist."
            abort(code, message)

        else:
            progress_list = Progress.query.filter(Progress.user_id == user_id).all()
            response = {
                "user_id": user_id,
                "progresses": progress_list,
                "count": len(progress_list)
            }
            return response

    @progress_ns.marshal_with(progress_model, code=201)
    @progress_ns.expect(progress_model)
    @requires_auth_with_same_user()
    def post(self, payload, user_id):
        '''Post a progress'''

        logger.info(f"POST request to track progress for {user_id} from {request.remote_addr}")
        try:
            user = User.query.get(user_id)
            if user is None:
                code = 404
                message = f"Cannot track progress for {user_id}. User does not exist."
            else:
                if api.payload["mood"].lower() not in valid_emotion_value:
                    raise ValueError("Mood does not contain valid value")
                if api.payload["diet"].lower() not in valid_emotion_value:
                    raise ValueError("Mood does not contain valid value")

                date = datetime.strptime(api.payload["track_date"], '%Y-%m-%d')
                if date.date() != datetime.today().date():
                    raise IllegalArgumentError()

                track_date = api.payload["track_date"]
                weight = api.payload["weight"]
                emotion = api.payload["mood"].lower()
                diet = api.payload["diet"].lower()
                api.payload["user_id"] = user_id
                progress = Progress(user_id=user_id, track_date=track_date, weight=weight,
                                    mood=emotion, diet=diet)
                progress.insert()
                code = 201

        except IllegalArgumentError:
            code = 422
            message = f"Progress can only be created for today {datetime.today().date()}"
        except ValueError:
            code = 400
            message = "Mood or Diet does not contain valid value of (Bad, Neutral, Good)"
        except IntegrityError:
            code = 422
            message = "Cannot add to existing progress. Use Patch request instead"
        except Exception as e:
            logger.debug(e)
            code = 400
            message = "The request data format is not valid"

        if code != 201:
            abort(code, message)

        return api.payload, 201

    @progress_ns.expect(progress_model)
    @progress_ns.response(204, 'Modify progress successful')
    @requires_auth_with_same_user()
    def patch(self, payload, user_id):
        '''Patch a progress'''

        logger.info(f"PATCH request to progress for {user_id} from {request.remote_addr}")
        try:
            user = User.query.get(user_id)
            if user is None:
                code = 404
                message = f"Cannot modify progress for {user_id}. User does not exist."
            else:
                if api.payload["mood"].lower() not in valid_emotion_value:
                    raise ValueError("Mood does not contain valid value")
                if api.payload["diet"].lower() not in valid_emotion_value:
                    raise ValueError("Mood does not contain valid value")

                track_date = api.payload["track_date"]
                weight = api.payload["weight"]
                emotion = api.payload["mood"].lower()
                diet = api.payload["diet"].lower()

                progress = Progress.query.filter(Progress.user_id == user_id) \
                    .filter(Progress.track_date == track_date).first()
                if progress is None:
                    code = 404
                    message = f"Cannot modify progress for {track_date}. This progress does not exist."
                else:
                    progress.weight = weight
                    progress.emotion = emotion
                    progress.diet = diet
                    progress.update()
                    code = 204

        except ValueError:
            code = 400
            message = "Mood or Diet does not contain valid value of (Bad, Neutral, Good)"
        except IntegrityError:
            code = 422
            message = "Cannot add to existing progress. Use Patch request instead"
        except Exception as e:
            logger.debug(e)
            code = 400
            message = "The request data format is not valid"

        if code != 204:
            abort(code, message)

        return '', 204
