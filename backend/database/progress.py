import enum

from sqlalchemy import Enum

from main import db
from dataclasses import dataclass

from datetime import datetime
from database.user import User

class Emotion(enum.Enum):
    Bad = -1
    Neutral = 0
    Good = 1

@dataclass
class Progress(db.Model):
    __tablename__ = 'progress'
    user_id: str = db.Column(db.String, db.ForeignKey('user.id'), primary_key=True, autoincrement=False)
    track_date: datetime = db.Column(db.DateTime, primary_key=True, nullable=False)
    weight: float = db.Column(db.Float, nullable=False)
    mood: Emotion = db.Column(Enum(Emotion), default=0, nullable=False)
    diet: Emotion = db.Column(Enum(Emotion), default=0, nullable=False)
