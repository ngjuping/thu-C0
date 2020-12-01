from mongoengine import *
import bson
import datetime
from Qinghuiyue.venus.models import Court
from Qinghuiyue.models.models import Stat
from Qinghuiyue.users.models import User
from Qinghuiyue import settings


class Feedback(DynamicDocument):
    user_id = IntField()
    time = DateTimeField()
    stars = IntField(min_value=1, max_value=5)
    content = StringField()
    reply = StringField()
    court = ObjectIdField()
    feedback_id = IntField()
    img = StringField()
    solved = BooleanField()

    # 要不要根据打星进行一个自动回复
    @classmethod
    def create_feedback(cls, params):
        # try:

        feedback = cls.objects.create(user_id=params['user_id'], court=Court.objects(court_id=params['court_id'])[0].id,
                                      content=params['content'], stars=params['stars'], time=datetime.datetime.now(),
                                      reply="等待管理员回复中", feedback_id=Stat.add_object("feedback"), solved=False)
        #img_name = settings.STATIC_URL + str(feedback.feedback_id) + params['img'].name
        img_name = "static/feedback/"+ str(feedback.feedback_id) + params['img'].name
        feedback.img = img_name
        feedback.save()
        with open(img_name, 'wb+') as img_file:
            for chunk in params['img'].chunks():
                img_file.write(chunk)
        user = User.objects(user_id=params['user_id'])[0]
        user.feedback.append(feedback.id)
        user.save()
        return True, feedback.feedback_id
    # except Exception:

    # return False,-1
