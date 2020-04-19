from datetime import datetime

from sqlalchemy.exc import IntegrityError

from main import api, logger

from flask_restx import Resource, abort

from flask import request

from models.progress import progress_model, progress_list_model
from database.progress import Progress, valid_emotion_value
from database.user import User

progress_ns = api.namespace('progress', description='Progress operations')


# @TODO: Verify if the subject token is the same as user-id (Authorization)

class IllegalArgumentError(ValueError):
    pass


@progress_ns.route('/<user_id>')
class ProgressList(Resource):

    @progress_ns.marshal_list_with(progress_list_model)
    def get(self, user_id):
        '''Get a list of user's progress'''

        logger.info(f"GET request to progress list of {user_id} from {request.remote_addr}")

        user = User.query.get(user_id)
        if user is None:
            code = 404
            message = f"Cannot track progress for {user_id}. User does not exist."
            abort(code, message)

        else:
            progresses = Progress.query.filter(Progress.user_id == user_id).all()
            response = {
                "user_id": user_id,
                "progresses": progresses,
                "count": len(progresses)
            }
            return response

    @progress_ns.marshal_with(progress_model)
    @progress_ns.expect(progress_model)
    def post(self, user_id):
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

    @progress_ns.marshal_with(progress_model)
    @progress_ns.expect(progress_model)
    def patch(self, user_id):
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
