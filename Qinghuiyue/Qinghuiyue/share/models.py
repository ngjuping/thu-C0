from mongoengine import *
from Qinghuiyue.reservation.models import Reservation
from Qinghuiyue.models.models import Stat
from Qinghuiyue.users.models import User
import datetime
class Share_notification(DynamicDocument):
    user_id=IntField()
    time=DateTimeField()
    content=StringField()
    reservation=ObjectIdField()
    status=IntField()
    share_id=IntField()

    @classmethod
    def create(cls,params):
        reservation=Reservation.objects(reservation_id=params['reservation_id']).first()
        if reservation:
            if reservation.status !=2:
                return False,{"message":"场地不符合拼场要求"}
            if len(cls.objects(reservation=reservation.id)):
                return False,{"message":"该预定已经发布拼场通知"}
            user = User.objects(user_id=params['user_id']).first()
            share=cls.objects.create(user_id=user.user_id,content=params['content'],
                               time=datetime.datetime.now(),reservation=reservation.id,
                               status=1,share_id=Stat.add_object("share_notification"))

            user.invitation.append(share)
            return True,{"message":"ok","share_id":share.share_id}
        else:
            return False,{"message":"找不到此预定"}
