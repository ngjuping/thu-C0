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
        #未付款、过期、已拼场的不符合要求
        if reservation:
            if reservation.status !=2:
                return False,{"message":"场地不符合拼场要求"}
            if reservation.details['start'] < datetime.datetime.now():
                return False,{"message": "该订单已经过期了"}
            if len(cls.objects(reservation=reservation.id)):
                return False,{"message":"该预定已经发布拼场通知"}

            user = User.objects(user_id=params['user_id']).first()
            share=cls.objects.create(user_id=user.user_id,content=params['content'],
                               time=datetime.datetime.now(),reservation=reservation.id,
                               status=1,share_id=Stat.add_object("share_notification"))

            user.invitation.append(share.id)
            user.save()
            return True,{"message":"ok","share_id":share.share_id}
        else:
            return False,{"message":"找不到此预定"}
    @classmethod
    def del_share(cls,reservation):
        '''
        传入reservation的objectID,如果有对应的拼场就删除
        '''
        share=cls.objects(reservation=reservation).first()
        if share:
            user=User.objects(user_id=share.user_id).first()
            user.invitation.remove(share.id)
            share.delete()

