from mongoengine import *
from datetime import  datetime,timedelta

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
    court_id=IntField()
    price=FloatField()
    matrix=ListField()
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
        #先获取下一周周一的日期
        now=datetime.now()+timedelta(days=1)#防止今天是周一

        while now.weekday()!=0:
            now+=timedelta(days=1)
        time=now.replace(hour=7,minute=0,second=0)
        time_end=time+timedelta(days=6,hours=15)
        i=0
        while i <len(self.Status):
            status=self.Status[i]
            if status['start'] >= time and status['end'] <= time_end:
                self.Status.pop(i)
            else:
                i+=1
        #应该要先处理掉可能冲突、重复的地方,但目前的处理不会通知到用户
        for i in range(15):
            for j in range(7):
                status={"start":time+timedelta(hours=i,days=j),"end":time+timedelta(hours=i+1,days=j),"user_id":-1,"code":self.matrix[i][j]}
                if status['code']==3:
                    status['users_id']=[]
                self.Status.append(status)
        self.save()

