from mongoengine import *
import bson
connect('qhy',host='58.87.86.11',port=27017)

class User(DynamicDocument):
    _id=ObjectIdField()
    user_id=IntField(required=True)
    name=StringField()
    api_id=IntField(required=True)
    password=StringField()
    rent_now=ListField()
    rent_history=ListField()
    invitation=ListField()
    feedback=ListField()

class Venue(DynamicDocument):
    _id=ObjectIdField()
    name=StringField()
    intro=StringField()
    courts=ListField()
    image=StringField()
    venue_id=IntField()

class  Court(DynamicDocument):
    _id = ObjectIdField()
    name=StringField()
    venue=ObjectIdField()
    status_now=StringField()
    enum_id=IntField()#运动类型
    rent_queue=ListField()
    draw_list=ListField()
    rent_for_long=ListField()
    Status=ListField()

class Feedback(DynamicDocument):
    _id=ObjectIdField()
    user_id=IntField()
    time=DateTimeField()
    stars=IntField(min_value=1,max_value=5)
    content=StringField()
    feedback=ListField()
    court=ObjectIdField()
    feedback_id=IntField()

class Notification(DynamicDocument):
    _id=ObjectIdField()
    time=DateTimeField()
    content=StringField()
    title=StringField()
    notice_id=IntField()

class Queue_reservation(DynamicDocument):
    _id=ObjectIdField()
    reservation_id=IntField()
    user_id=IntField()
    sport_type=IntField()
    day=StringField()
    time_from=StringField()
    time_to=StringField()
    status=StringField()
    type=IntField()#抽签方式？

class Reservation(DynamicDocument):
    _id=ObjectIdField()
    type=IntField()
    paras=DictField()
    status=StringField()
    reservation_id=IntField()

class Share_notification(DynamicDocument):
    _id=ObjectIdField()
    user_id=IntField()
    time=DateTimeField()
    content=StringField()
    reservation=ObjectIdField()
    status=StringField()
    share_id=IntField()

class Course(DynamicDocument):
    _id=ObjectIdField()
    name=StringField()
    date=DateField()
    time=StringField()
    position=StringField()
    description=StringField()
    price=StringField()
    course_id=IntField()


for i in Reservation.objects:
    print(i['paras'])