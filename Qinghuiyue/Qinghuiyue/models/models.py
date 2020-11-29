from mongoengine import *
import bson
import bcrypt

class Feedback(DynamicDocument):
    user_id=IntField()
    time=DateTimeField()
    stars=IntField(min_value=1,max_value=5)
    content=StringField()
    feedback=ListField()
    court=ObjectIdField()
    feedback_id=IntField()
    img=StringField()
class Notification(DynamicDocument):
    time=DateTimeField()
    content=StringField()
    title=StringField()
    notice_id=IntField()

class Queue_reservation(DynamicDocument):
    reservation_id=IntField()
    user_id=IntField()
    sport_type=IntField()
    day=StringField()
    time_from=StringField()
    time_to=StringField()
    status=StringField()
    type=IntField()#抽签方式？

class Reservation(DynamicDocument):
    type=IntField()
    details=DictField()
    status=IntField()
    reservation_id=IntField()


class Share_notification(DynamicDocument):
    user_id=IntField()
    time=DateTimeField()
    content=StringField()
    reservation=ObjectIdField()
    status=StringField()
    share_id=IntField()

class Course(DynamicDocument):
    name=StringField()
    date=DateField()
    time=StringField()
    position=StringField()
    description=StringField()
    price=StringField()
    course_id=IntField()

class Stat(DynamicDocument):
    data=DictField()
    name=StringField()