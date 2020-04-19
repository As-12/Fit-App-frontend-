from main import api
from flask_restx import fields

user_model = api.model('user_model', {
    'id': fields.String(description='IdP provided user-id'),
    'target_weight': fields.Float(description='User target weight', required=False),
    'dob': fields.Date(description='Date of birth', required=False),
    'city': fields.String(description='City', required=False),
    'state': fields.String(description='State or Country (Non-US)', required=False)
})

user_patch_model = api.model('user_patch_model', {
    'target_weight': fields.Float(description='User target weight', required=False),
    'dob': fields.Date(description='Date of birth', required=False),
    'city': fields.String(description='City', required=False),
    'state': fields.String(description='State or Country (Non-US)', required=False)
})

user_list_model = api.model('user_list_model', {
        'users': fields.List(fields.Nested(user_model), default=[]),
        'count': fields.Integer(readonly=True, description='Total number of users')
})