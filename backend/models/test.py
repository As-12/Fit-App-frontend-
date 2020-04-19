from main import api
from flask_restx import fields

test_model = api.model('test_model', {
        'message': fields.String(description='A test message')
})
