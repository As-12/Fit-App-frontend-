import enum

from sqlalchemy import Enum

from main import db
from dataclasses import dataclass

from datetime import datetime
import database

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

    def insert(self):
        """
       insert()
           inserts a new model into a database
           the model must have a unique name
           the model must have a unique id or null id
           EXAMPLE
               progress = Progress(user_id=user_id, track_date=Date())
               progress.insert()
        """
        try:
            self.validate()
            # You can only insert today's progress
            date = datetime.strptime(self.track_date, '%Y-%m-%d')
            if date.date() != datetime.today().date():
                raise ValueError("You can only track progress for today")
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise
        finally:
            db.session.close()

    def delete(self):
        """
       delete()
           deletes a new model into a database
           the model must exist in the database
           EXAMPLE
               progress = Progress(user_id=user_id, track_date=Date())
               progress.delete()
        """
        db.session.delete(self)
        db.session.commit()
        db.session.close()

    def update(self, update_dict=None):
        """
       update()
           updates a new model into a database
           the model must exist in the database
           EXAMPLE
               progress = Progress(user_id=user_id)
               progress.weight = 200.5
               progress.update()
        """
        try:
            self.validate()
            if update_dict is not None:
                self.weight = update_dict["weight"]
                self.mood = update_dict["mood"].lower()
                self.diet = update_dict["diet"].lower()
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()

    def validate(self):
        """
       validate()
           Validate the model for invalid value.
           Raise a ValueError for invalid value
           This function is automatically called upon insert or update
        """
        if self.mood.lower() not in valid_emotion_value:
            raise ValueError("Mood does not contain valid value")
        if self.diet.lower() not in valid_emotion_value:
            raise ValueError("Diet does not contain valid value")

    def insert_test(self):
        """
               insert_test()
                  test method to be used to insert test data
        """
        try:
            self.validate()
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise
        finally:
            db.session.close()