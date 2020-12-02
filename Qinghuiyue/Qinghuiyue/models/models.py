from mongoengine import *
import bson
import bcrypt
from Qinghuiyue.venus.models import Court




class Notification(DynamicDocument):
    time = DateTimeField()
    content = StringField()
    title = StringField()
    notice_id = IntField()





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
