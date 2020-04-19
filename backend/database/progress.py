import enum

from sqlalchemy import Enum

from main import db
from dataclasses import dataclass

from datetime import datetime
from database.user import User


# List of valid emotional value. Enum is preferred but not supported by Marshmallow
valid_emotion_value = ["bad", "neutral", "good"]


@dataclass
class Progress(db.Model):
    __tablename__ = 'progress'
    user_id: str = db.Column(db.String, db.ForeignKey('user.id'), primary_key=True, autoincrement=False)
    track_date: datetime = db.Column(db.DateTime, primary_key=True, nullable=False)
    weight: float = db.Column(db.Float, nullable=False)
    mood: str = db.Column(db.String, default="neutral", nullable=False)
    diet: str = db.Column(db.String, default="neutral", nullable=False)

    '''
        insert()
            inserts a new model into a database
            the model must have a unique name
            the model must have a unique id or null id
            EXAMPLE
                progress = Progress(user_id=user_id, track_date=Date())
                progress.insert()
        '''

    def insert(self):
        try:
            if self.mood not in valid_emotion_value:
                raise ValueError("Mood value is invalid")
            if self.diet not in valid_emotion_value:
                raise ValueError("Diet value is invalid")
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            raise
        finally:
            db.session.close()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            progress = Progress(user_id=user_id, track_date=Date())
            progress.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        db.session.close()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            progress = Progress(user_id=user_id)
            progress.weight = 200.5 
            progress.update()
    '''

    def update(self):
        try:
            if self.mood not in valid_emotion_value:
                raise ValueError("Mood value is invalid")
            if self.diet not in valid_emotion_value:
                raise ValueError("Diet value is invalid")
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
