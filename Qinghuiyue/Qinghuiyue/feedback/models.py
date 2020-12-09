from mongoengine import *
import bson
import datetime
from Qinghuiyue.venus.models import Court
from Qinghuiyue.models.models import Stat
from Qinghuiyue.users.models import User
from Qinghuiyue import settings
from Qinghuiyue.reservation.models import Reservation


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
    reservation_id=IntField()#对应的预定，一个预定只能反馈一次
    # 要不要根据打星进行一个自动回复
    @classmethod
    def create_feedback(cls, params):
        try:
            feedback=cls.objects(reservation_id=params['reservation_id']).first()
            if feedback:
                return False,"已经反馈过啦！"
            reservation=Reservation.objects(reservation_id=params['reservation_id']).first()
            feedback = cls.objects.create(user_id=params['user_id'], court=reservation.details['court'],
                                          content=params['content'], stars=params['stars'], time=datetime.datetime.now(),
                                          reply="等待管理员回复中", feedback_id=Stat.add_object("feedback"), reservation_id=params['reservation_id'],solved=False)
            #img_name = settings.STATIC_URL + str(feedback.feedback_id) + params['img'].name
            if params['img']:
                img_name = "static/feedback/"+ str(feedback.feedback_id) + params['img'].name
                feedback.img = img_name
                feedback.save()

                with open(img_name, 'wb+') as img_file:
                    for chunk in params['img'].chunks():
                        img_file.write(chunk)
            else:
                feedback.img="None"
                feedback.save()
            user = User.objects(user_id=params['user_id'])[0]
            user.feedback.append(feedback.id)
            user.save()
            return True, feedback.feedback_id
        except Exception:

            return False,"创建反馈失败！系统内部错误"
