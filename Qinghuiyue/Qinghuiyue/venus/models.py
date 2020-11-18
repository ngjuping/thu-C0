from mongoengine import *
import bson
import bcrypt

class Venue(DynamicDocument):
    name=StringField()
    intro=StringField()
    courts=ListField()
    image=StringField()
    venue_id=IntField()
    notices=ListField()

class Court(DynamicDocument):
    name=StringField()
    venue=ObjectIdField()
    status_now=StringField()
    enum_id=IntField()#运动类型
    rent_queue=ListField()
    draw_list=ListField()
    rent_for_long=ListField()
    Status=ListField()