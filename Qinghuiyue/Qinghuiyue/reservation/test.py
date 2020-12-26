from datetime import datetime

from mongoengine import connect, disconnect

from Qinghuiyue.reservation.models import Reservation
from Qinghuiyue.users.models import User
from Qinghuiyue.models.models import Stat
from Qinghuiyue.test import NoSQLTestCase
from Qinghuiyue.venues.models import Venue,Court


class ReservationViewTest(NoSQLTestCase):

    @classmethod
    def setUpClass(cls):
        '''
        在该函数中定义需要用到的模型，必须要先disconnect然后连接mock.之后的
        定义要多少自己定
        '''
        disconnect()
        connect('mongoenginetest', host='mongomock://localhost')
        Stat.objects.create(name='size_of_collection', data={'user': 0, 'venue': 0
                                                             , 'court': 0, 'feedback': 0,
                                                             'notification': 0, 'share_notification': 0,
                                                             'reservation': 0, 'course': 0})

        user=User.create(password='123abc', user_id=Stat.add_object("user"), name='test',
                    api_id='2018000001', privilege=0)
        user2=User.create(password='123abc', user_id=Stat.add_object("user"), name='test',
                    api_id='2018000002', privilege=0)
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
                                                        'created':datetime.now(),'paid_at':datetime.now()})#已经付款，用来转让
        reservation2=Reservation.objects.create(type=1,status=5,reservation_id=Stat.add_object("reservation"),
                                               details={"court":court.id,"user_id":user.user_id,
                                                        'start':datetime(2021,12,25,8),'end':datetime(2021,12,25,9),
                                                        'created':datetime.now()})
        reservation3=Reservation.objects.create(type=1,status=2,reservation_id=Stat.add_object("reservation"),
                                               details={"court":court.id,"user_id":user.user_id,
                                                        'start':datetime(2020,11,25,8),'end':datetime(2020,11,25,9),
                                                        'created':datetime.now(),'paid_at':datetime.now()})#过期
        reservation4=Reservation.objects.create(type=1,status=1,reservation_id=Stat.add_object("reservation"),
                                               details={"court":court.id,"user_id":user.user_id,
                                                        'start':datetime(2021,12,25,7),'end':datetime(2021,12,25,8),
                                                        'created':datetime.now(),'paid_at':datetime.now()})#用于取消
        user.rent_now.append(reservation.id)
        user.rent_now.append(reservation2.id)
        user.rent_now.append(reservation3.id)
        user.rent_now.append(reservation4.id)
        user.save()

    @classmethod
    def tearDownClass(cls):
        '''
        断开假服务器，数据不会保存
        '''
        disconnect()

    def test_get_reservation(self):
        '''
        测不在线与在线
        '''
        response=self.client.get('/api/manage/courts?user_id=1')
        self.assertEqual(response.status_code,403)
        self.client.post('/api/login', {'api_id': '2018000001', 'pwd': '123abc'},
                         content_type='application/json')
        response=self.client.get('/api/manage/courts?user_id=1')
        self.assertEqual(response.status_code,200)

    def test_book_draw(self):
        '''
        没登陆，无预定时间段、预定成功、已经预定过、参加过多抽签
        '''
        self.client.post('/api/logout')
        response = self.client.post('/api/draw',{'court_id':1,'start':'2021-12-24T9:00:00',
                                                'end':'2021-12-24T10:00:00'},content_type='application/json')
        self.assertEqual(response.status_code,403)

        self.client.post('/api/login', {'api_id': '2018000001', 'pwd': '123abc'},
                         content_type='application/json')
        response = self.client.post('/api/draw',{'court_id':1,'start':'2021-12-24T9:00:00',
                                                'end':'2021-12-24T10:00:00'},content_type='application/json')
        self.assertEqual(response.status_code,400)
        response = self.client.post('/api/draw', {'court_id': 1, 'start': '2021-12-25T9:00:00',
                                                 'end': '2021-12-25T10:00:00'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        #之后再定一个，数据库里已经有一个
        response = self.client.post('/api/draw', {'court_id': 1, 'start': '2021-12-25T10:00:00',
                                                 'end': '2021-12-25T11:00:00'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        #已经订过
        response = self.client.post('/api/draw', {'court_id': 1, 'start': '2021-12-25T9:00:00',
                                                 'end': '2021-12-25T10:00:00'}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        #参加过多
        response = self.client.post('/api/draw', {'court_id': 1, 'start': '2021-12-25T12:00:00',
                                                 'end': '2021-12-25T13:00:00'}, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_book_first_come(self):
        '''
        没登陆，没有时间段，成功
        '''
        self.client.post('/api/logout')
        response = self.client.post('/api/book',{'court_id':1,'start':'2021-12-25T13:00:00',
                                                'end':'2021-12-25T14:00:00'},content_type='application/json')
        self.assertEqual(response.status_code,403)

        self.client.post('/api/login', {'api_id': '2018000001', 'pwd': '123abc'},
                         content_type='application/json')
        response = self.client.post('/api/book',{'court_id':1,'start':'2021-12-25T12:00:00',
                                                'end':'2021-12-25T13:00:00'},content_type='application/json')
        self.assertEqual(response.status_code,400)
        response = self.client.post('/api/book',{'court_id':1,'start':'2021-12-25T13:00:00',
                                                'end':'2021-12-25T14:00:00'},content_type='application/json')
        self.assertEqual(response.status_code,200)

    def test_transfer_reservation(self):
        '''
        无订单，订单不可可以转让，已过期，无转移权限，无目标用户，成功
        '''
        self.client.post('/api/login', {'api_id': '2018000001', 'pwd': '123abc'},
                         content_type='application/json')
        response=self.client.post('/api/manage/reservation/transfer',{"new_user_id":2,"reservation_id":10},content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response=self.client.post('/api/manage/reservation/transfer',{"new_user_id":2,"reservation_id":2},content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response=self.client.post('/api/manage/reservation/transfer',{"new_user_id":2,"reservation_id":3},content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.client.post('/api/logout')
        self.client.post('/api/login', {'api_id': '2018000002', 'pwd': '123abc'},
                         content_type='application/json')
        response=self.client.post('/api/manage/reservation/transfer',{"new_user_id":2,"reservation_id":1},content_type='application/json')
        self.assertEqual(response.status_code, 400)

        self.client.post('/api/logout')
        self.client.post('/api/login', {'api_id': '2018000001', 'pwd': '123abc'},
                         content_type='application/json')
        response=self.client.post('/api/manage/reservation/transfer',{"new_user_id":3,"reservation_id":1},content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response=self.client.post('/api/manage/reservation/transfer',{"new_user_id":2,"reservation_id":1},content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_cancel_reservation(self):
        '''
        找不到订单，无权限，当前不可以取消，成功
        '''
        self.client.post('/api/login', {'api_id': '2018000001', 'pwd': '123abc'},
                         content_type='application/json')
        response=self.client.post('/api/manage/reservation/cancel',{"reservation_id":10},content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.client.post('/api/logout')
        self.client.post('/api/login', {'api_id': '2018000002', 'pwd': '123abc'},
                         content_type='application/json')
        response=self.client.post('/api/manage/reservation/cancel',{"reservation_id":10},content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.client.post('/api/logout')
        self.client.post('/api/login', {'api_id': '2018000001', 'pwd': '123abc'},
                         content_type='application/json')
        response=self.client.post('/api/manage/reservation/cancel',{"reservation_id":1},content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response=self.client.post('/api/manage/reservation/cancel',{"reservation_id":4},content_type='application/json')
        self.assertEqual(response.status_code, 200)