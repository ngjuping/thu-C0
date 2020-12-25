from datetime import datetime

from mongoengine import connect, disconnect

from Qinghuiyue.reservation.models import Reservation
from Qinghuiyue.users.models import User
from Qinghuiyue.models.models import Stat
from Qinghuiyue.test import NoSQLTestCase
from Qinghuiyue.venues.models import Venue,Court
from Qinghuiyue.feedback.models import Feedback
class FeedbackViewTest(NoSQLTestCase):
    @classmethod
    def setUpClass(cls):
        disconnect()
        connect('mongoenginetest', host='mongomock://localhost')
        Stat.objects.create(name='size_of_collection', data={'user': 0, 'venue': 0
                                                             , 'court': 0, 'feedback': 0,
                                                             'notification': 0, 'share_notification': 0,
                                                             'reservation': 0, 'course': 0})

        user=User.create(password='123abc', user_id=Stat.add_object("user"), name='test',
                    api_id='2018000001', privilege=0)
        user2=User.create(password='123abc', user_id=Stat.add_object("user"), name='test',
                    api_id='2018000002', privilege=1)
        user3=User.create(password='123abc', user_id=Stat.add_object("user"), name='test',
                    api_id='2018000003', privilege=0)
        venue=Venue.objects.create(name="击剑场",intro="击剑的场地",image="img",venue_id=Stat.add_object("venue"))
        court=Court.objects.create(name="击剑一号",venue=venue.id,status_now="开放",enum_id=1,
                                   Status=[{'start':datetime(2021,12,25,7),'end':datetime(2021,12,25,8),"user_id":user.user_id,"code":2},
                                           {'start':datetime(2021,12,25,8),'end':datetime(2021,12,25,9),"user_id":user.user_id,"code":2},
                                           {'start':datetime(2021,12,25,9),'end':datetime(2021,12,25,10),"user_id":-1,"code":3,"reservation_ids":[],"users_id":[]},
                                           {'start':datetime(2021,12,25,10),'end':datetime(2021,12,25,11),"user_id":-1,"code":3,"reservation_ids":[],"users_id":[]},
                                           {'start':datetime(2021,12,25,11),'end':datetime(2021,12,25,12),"user_id":-1,"code":3,"reservation_ids":[],"users_id":[]},
                                           {'start':datetime(2021,12,25,12),'end':datetime(2021,12,25,13),"user_id":-1,"code":3,"reservation_ids":[],"users_id":[]},
                                           {'start':datetime(2021,12,25,13),'end':datetime(2021,12,25,14),"user_id":-1,"code":1}],
                                   court_id=Stat.add_object("court"),price=15)
        venue.courts.append(court)
        venue.save()
        reservation=Reservation.objects.create(type=1,status=2,reservation_id=Stat.add_object("reservation"),
                                               details={"court":court.id,"user_id":user.user_id,
                                                        'start':datetime(2021,12,25,7),'end':datetime(2021,12,25,8),
                                                        'created':datetime.now(),'paid_at':datetime.now()})#已经付款
        reservation2=Reservation.objects.create(type=1,status=5,reservation_id=Stat.add_object("reservation"),
                                               details={"court":court.id,"user_id":user.user_id,
                                                        'start':datetime(2021,12,20,8),'end':datetime(2021,12,20,9),
                                                        'created':datetime.now()})#过期,已经创建反馈
        reservation3=Reservation.objects.create(type=1,status=2,reservation_id=Stat.add_object("reservation"),
                                               details={"court":court.id,"user_id":user.user_id,
                                                        'start':datetime(2020,11,25,8),'end':datetime(2020,11,25,9),
                                                        'created':datetime.now(),'paid_at':datetime.now()})#过期,可以用来创建反馈
        feedback=Feedback.objects.create(user_id=1,time=datetime.now,stars=5,content="<p>很好，五星好评蛤蛤蛤哈</p>",
                                         reply="wu",court=court.id,feedback_id=Stat.add_object("feedback"),
                                         img="None",solved=False,reservation_id=reservation2.reservation_id)
        feedback2=Feedback.objects.create(user_id=1,time=datetime.now,stars=5,content="<p>很好，五星好评蛤蛤蛤哈</p>",
                                         reply="wu",court=court.id,feedback_id=Stat.add_object("feedback"),
                                         img="None",solved=False,reservation_id=reservation3.reservation_id)#用来删除
        user.rent_now.append(reservation.id)
        user.rent_now.append(reservation2.id)
        user.rent_now.append(reservation3.id)
        user.feedback.append(feedback.id)
        user.feedback.append(feedback2.id)
        user.save()
    @classmethod
    def tearDownClass(cls):
        '''
        断开假服务器，数据不会保存
        '''
        disconnect()

    def test_get_all_feedback(self):
        response=self.client.get('/api/manage/feedback?page=1&size=5')
        self.assertEqual(response.status_code,200)

    def test_get_user_feedback(self):
        '''
        没有用户，成功
        '''
        response=self.client.get('/api/manage/feedback/user?user_id=10&page=1&size=5')
        self.assertEqual(response.status_code,400)
        response=self.client.get('/api/manage/feedback/user?user_id=1&page=1&size=5')
        self.assertEqual(response.status_code,200)


    def test_delete_feedback(self):
        '''
        找不到反馈，无权限，成功
        '''
        self.client.post('/api/login', {'api_id': '2018000003', 'pwd': '123abc'},
                         content_type='application/json')
        response=self.client.post('/api/manage/feedback/delete',{'feedback_id':10},content_type='application/json')
        self.assertEqual(response.status_code, 500)
        response=self.client.post('/api/manage/feedback/delete',{'feedback_id':2},content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.client.post('/api/logout')
        self.client.post('/api/login', {'api_id': '2018000001', 'pwd': '123abc'},
                         content_type='application/json')
        response=self.client.post('/api/manage/feedback/delete',{'feedback_id':2},content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_reply_feedback(self):
        '''
        无权限，找不到，成功
        '''
        self.client.post('/api/login', {'api_id': '2018000003', 'pwd': '123abc'},
                         content_type='application/json')
        response=self.client.post('/api/admin/reply/feedback',{'feedback_id':1,"reply":"ok","solved":True},content_type='application/json')
        self.assertEqual(response.status_code,403)
        self.client.post('/api/logout')
        self.client.post('/api/login', {'api_id': '2018000002', 'pwd': '123abc'},
                         content_type='application/json')
        response=self.client.post('/api/admin/reply/feedback',{'feedback_id':10,"reply":"ok","solved":True},content_type='application/json')
        self.assertEqual(response.status_code,500)
        response = self.client.post('/api/admin/reply/feedback', {'feedback_id': 1, "reply": "ok", "solved": True},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)


