from main import api

from flask_restx import Resource

from database.question import Question
from models.test import test_model


test_ns = api.namespace('test', description='test operations')

@test_ns.marshal_list_with(test_model)
@test_ns.route('/')
class CategoryList(Resource):
    '''Shows a list of all categories'''

    def get(self):
        '''Get sample message'''
        result = Question.query.all()

        response = {
            "message": "Hi",
        }
        return response