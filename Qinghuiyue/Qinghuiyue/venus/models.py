from random import randint
from mongoengine import *
from datetime import datetime, timedelta


class Venue(DynamicDocument):
    name = StringField()
    intro = StringField()
    courts = ListField()
    image = StringField()
    venue_id = IntField()
    notices = ListField()


class Court(DynamicDocument):

    name = StringField()
    venue = ObjectIdField()
    status_now = StringField()
    enum_id = IntField()  # 运动类型
    rent_queue = ListField()
    draw_list = ListField()
    rent_for_long = ListField()
    Status = ListField()
    court_id = IntField()
    price = FloatField()
    matrix = ListField()

    def set_schedule(self):
        """
         matrix:[
         [1,2,3,1,2,2,3],
         [1,2,3,1,2,2,3],
         ...
         ]#大小7*15，15代表十五个时间段，7-8,8-9...21-22
        根据这个矩阵把下一周的场地全部安排好
        注意，0是代表周一
         """

        if not self.matrix:
            return
        # 先获取下一周周一的日期
        now = datetime.now() + timedelta(days=1)  # 防止今天是周一

        while now.weekday() != 0:
            now += timedelta(days=1)
        time = now.replace(hour=7, minute=0, second=0, microsecond=0)
        time_end = time + timedelta(days=6, hours=15)
        i = 0
        print(self.court_id)
        while i < len(self.Status):

            status = self.Status[i]
            print(status)
            if status['start'] >= time and status['end'] <= time_end:
                self.Status.pop(i)
            else:
                i += 1
        # 应该要先处理掉可能冲突、重复的地方,但目前的处理不会通知到用户
        for i in range(15):
            for j in range(7):
                status = {"start": time + timedelta(hours=i, days=j), "end": time + timedelta(hours=i + 1, days=j),
                          "user_id": -1, "code": self.matrix[i][j]}
                if status['code'] == 3:
                    status['reservation_ids'] = []  # 存储reservation的id
                    status['users_id']=[]#储存定了了user_id
                self.Status.append(status)
        self.save()

    def draw(self):
        '''
        执行抽签，对所有下周可抽签场地执行。
        '''
        from Qinghuiyue.reservation.models import Reservation
        for status in self.Status:
            # 供抽签且有人参与才抽，如果没人参与的话就直接变成可先到先得
            if status['code'] == 3:
                if len(status['reservation_ids']):
                    bingo = randint(0, len(status['reservation_ids']))
                    bingo_id = status['reservation_ids'].pop(bingo)
                    reservation = Reservation.objects(id=bingo_id).first()
                    reservation.status = 1
                    status['user_id'] = reservation.details['user_id']
                    reservation.save()
                    for reservation_id in status['reservation_ids']:
                        reservation = Reservation.objects(id=reservation_id).first()
                        reservation.status = 6
                        reservation.save()
                    status.pop('reservation_ids', None)
                    status.pop('users_id',None)
                    status['code'] = 2
                else:
                    status['code'] = 1

        self.save()

