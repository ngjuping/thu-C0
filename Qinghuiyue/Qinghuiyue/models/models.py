from mongoengine import *
import bson
import bcrypt
from Qinghuiyue.venus.models import Court




class Notification(DynamicDocument):
    time = DateTimeField()
    content = StringField()
    title = StringField()
    notice_id = IntField()


class Queue_reservation(DynamicDocument):
    reservation_id = IntField()
    user_id = IntField()
    sport_type = IntField()
    day = StringField()
    time_from = StringField()
    time_to = StringField()
    status = StringField()
    type = IntField()  # 抽签方式？


class Reservation(DynamicDocument):
    type = IntField()
    details = DictField()
    status = IntField()
    reservation_id = IntField()

    @classmethod
    def get_reservation_info(cls, objectID):
        rent = cls.objects(id=objectID).first()
        if rent:
            return {
                "reservation_id": rent.reservation_id,
                "type": rent.type,
                "status": rent.status,
                "details": {
                    "name": Court.objects(id=rent.details['court'])[0].name,
                    "start": rent.details['start'],
                    "end": rent.details['end']
                }
            }


class Course(DynamicDocument):
    name = StringField()
    date = DateField()
    time = StringField()
    position = StringField()
    description = StringField()
    price = StringField()
    course_id = IntField()


class Stat(DynamicDocument):
    data = DictField()
    name = StringField()
    @classmethod
    def add_object(cls,objType):
        '''

        :param objType:字符串，如user,会增加一个user并返回增加后的id
        :return:
        '''
        stat=cls.objects(name="size_of_collection")[0]
        stat.data[objType]+=1
        stat.save()
        return stat.data[objType]
