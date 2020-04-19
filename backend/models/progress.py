from main import api
from flask_restx import fields

progress_model = api.model('progress_model', {
    'track_date': fields.Date(description='Date of tracking', required=True, format='%Y-%m-%d'),
    'weight': fields.Float(description='Current weight', required=True),
    'mood': fields.String(description='Mood value. Can be one of the following (neutral, bad, good)',
                          required=True, default="neutral"),
    'diet': fields.String(description='Diet value. Can be one of the following (neutral, bad, good)',
                          required=True, default="neutral")
})

progress_list_model = api.model('progress_list_model', {
    'user_id': fields.String(description='IdP provided user-id'),
    'progresses': fields.List(fields.Nested(progress_model), default=[]),
    'count': fields.Integer(readonly=True, description='Progress counts')
})
