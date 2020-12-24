from random import randint
from copy import deepcopy
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
    def set_future_court(self,weeks=1):
        """
        根据现有的matrix来设定后weeks周的场地
        如果有场地已经有人预定，会跳过这些将带来冲突的场地
        weeks=1代表下一周
         matrix:[
         [1,2,3,1,2,2,3],
         [1,2,3,1,2,2,3],
         ...
         ]#大小7*15，15代表十五个时间段，7-8,8-9...21-22
        根据这个矩阵把下下周的场地全部安排好
        注意，0是代表周一
        """
        if not self.matrix:
            return
        # 先获取下一周周一的日期
        now = datetime.now() + timedelta(days=1+(weeks-1)*7)  # 防止今天是周一

        while now.weekday() != 0:
            now += timedelta(days=1)
        time = now.replace(hour=7, minute=0, second=0, microsecond=0)
        time_end = time + timedelta(days=6, hours=15)
        i = 0
        matrix=deepcopy(self.matrix)
        #已经安排过的场地不会自动安排，自动安排时会跳过，防止给用户预定带来冲突
        while i < len(self.Status):
            status = self.Status[i]
            if status['start'] >= time and status['end'] <= time_end:
                matrix[status['start'].hour-time.hour][(status['start']-time).days]=-1
                self.Status.pop(i)
            else:
                i += 1
        for i in range(15):
            for j in range(7):
                if matrix[i][j]==-1:
                    print("skip")
                    continue

                status = {"start": time + timedelta(hours=i, days=j), "end": time + timedelta(hours=i + 1, days=j),
                          "user_id": -1, "code": self.matrix[i][j]}
                if status['code'] == 3:
                    status['reservation_ids'] = []  # 存储reservation的id
                    status['users_id']=[]#储存定了了user_id
                self.Status.append(status)
        self.save()

    def set_schedule(self):
        """
        设定下下周与下周的场地
        """
        self.set_future_court(1)
        self.set_future_court(2)

    def draw(self):
        '''
        执行抽签，对所有下周可抽签场地执行。
        '''
        from Qinghuiyue.reservation.models import Reservation
        now = datetime.now() + timedelta(days=1)  # 防止今天是周一
        while now.weekday() != 0:
            now += timedelta(days=1)
        time = now.replace(hour=7, minute=0, second=0, microsecond=0)
        time_end = time + timedelta(days=6, hours=15)
        for status in self.Status:
            # 供抽签且有人参与才抽，如果没人参与的话就直接变成可先到先得
            if status['code'] == 3 and status['start']>=time and status['end']<=time_end:
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

