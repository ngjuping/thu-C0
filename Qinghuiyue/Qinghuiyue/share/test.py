from datetime import datetime
from mongoengine import connect, disconnect
from Qinghuiyue.users.models import User
from Qinghuiyue.models.models import Stat
from Qinghuiyue.share.models import Share_notification
from Qinghuiyue.test import NoSQLTestCase
from Qinghuiyue.reservation.models import Reservation
from Qinghuiyue.venues.models import Venue,Court

class ShareViewTest(NoSQLTestCase):

    @classmethod
    def setUpClass(cls):
        disconnect()
        connect('mongoenginetest', host='mongomock://localhost')
        Stat.objects.create(name='size_of_collection', data={'user': 0, 'venue': 0,
                                                             'court': 0, 'feedback': 0,
                                                             'notification': 0, 'share_notification': 0,
                                                             'reservation': 0, 'course': 0})
        user=User.create(password='123abc', user_id=Stat.add_object("user"), name='test',
                    api_id='2018000001', privilege=0)
        user2=User.create(password='123abc', user_id=Stat.add_object("user"), name='test',
                    api_id='2018000002', privilege=0)
        venue=Venue.objects.create(name="击剑场",intro="击剑的场地",image="img",venue_id=Stat.add_object("venue"))
        court=Court.objects.create(name="击剑一号",venue=venue.id,status_now="开放",enum_id=1,
                                   Status=[{'start':datetime(2021,12,25,7),'end':datetime(2021,12,25,8),"user_id":user.user_id,"code":2},
                                           {'start':datetime(2021,12,25,8),'end':datetime(2021,12,25,9),"user_id":user.user_id,"code":2}],
                                   court_id=Stat.add_object("court"),price=15)
        venue.courts.append(court)
        venue.save()
        reservation=Reservation.objects.create(type=1,status=2,reservation_id=Stat.add_object("reservation"),
                                               details={"court":court.id,"user_id":user.user_id,
                                                        'start':datetime(2021,12,25,7),'end':datetime(2021,12,25,8),
                                                        'created':datetime.now(),'paid_at':datetime.now()})
        reservation2=Reservation.objects.create(type=1,status=2,reservation_id=Stat.add_object("reservation"),
                                               details={"court":court.id,"user_id":user.user_id,
                                                        'start':datetime(2021,12,25,8),'end':datetime(2021,12,25,9),
                                                        'created':datetime.now(),'paid_at':datetime.now()})
        share=Share_notification.objects.create(user_id=user.user_id,time=datetime.now(),content="<p>很不错的场地</p>",
                                               reservation=reservation.id,img="None",share_id=Stat.add_object("share_notification"))
        share_to_be_delete=Share_notification.objects.create(user_id=user.user_id,time=datetime.now(),content="<p>很不错的场地</p>",
                                               reservation=reservation.id,img="None",share_id=Stat.add_object("share_notification"))
        user.invitation.append(share.id)
        user.rent_now.append(reservation.id)
        user.rent_now.append(reservation2.id)
        user.save()
    @classmethod
    def tearDownClass(cls):
        '''
        断开假服务器，数据不会保存
        '''
        disconnect()

    def test_get_share_notifications(self):
        response=self.client.get('/api/manage/share?page=1&size=5')
        self.assertEqual(response.status_code,200)
        response=self.client.get('/api/manage/share?page=1&size=1')
        self.assertEqual(response.status_code,200)
    def test_get_user_shares(self):
        self.client.post('/api/logout')
        response = self.client.get('/api/manage/share/user?user_id=1&page=1&size=5')#没登陆
        self.assertEqual(response.status_code, 403)
        self.client.post('/api/login', {'api_id': '2018000001', 'pwd': '123abc'},
                                    content_type='application/json')
        response = self.client.get('/api/manage/share/user?user_id=1&page=1&size=5')#登陆后
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/manage/share/user?user_id=1&page=1&size=1')#页数
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/manage/share/user?user_id=10&page=1&size=5')  # 不存在
        self.assertEqual(response.status_code, 400)

    def test_create_share(self):
        '''
        测试了重复、字数错误、用户验证错误、成功
        '''
        self.client.post('/api/login', {'api_id': '2018000001', 'pwd': '123abc'},
                         content_type='application/json')
        response=self.client.post('/api/manage/share/create',{'user_id':1,'content':'<p>一起来玩耍吗？等你来呃</p>','reservation_id':1},content_type='application/json')
        self.assertEqual(response.status_code,400)
        response = self.client.post('/api/manage/share/create',
                                    {'user_id': 1, 'content': '<p>一起来玩耍吗？</p>', 'reservation_id': 2},content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/api/manage/share/create',
                                    {'user_id': 2, 'content': '<p>一起来玩耍吗？</p>', 'reservation_id': 2},content_type='application/json')
        self.assertEqual(response.status_code, 403)
        response = self.client.post('/api/manage/share/create',
                                    {'user_id': 1, 'content': '<p>一起来玩耍吗？等你来呃</p>', 'reservation_id': 2},content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_update_share(self):
        '''
        测试了长度不对，成功，身份验证不对
        '''
        self.client.post('/api/login', {'api_id': '2018000001', 'pwd': '123abc'},
                         content_type='application/json')
        response=self.client.post('/api/manage/share/update',{'share_id':1,'content':'<p>一起来玩耍吗</p>'},content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/api/manage/share/update', {'share_id': 1, 'content': '<p>一起来玩耍吗?等你来呃</p>'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.client.post('/api/logout')
        self.client.post('/api/login', {'api_id': '2018000002', 'pwd': '123abc'},
                         content_type='application/json')
        response = self.client.post('/api/manage/share/update', {'share_id': 1, 'content': '<p>一起来玩耍吗?等你来呃</p>'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_delete_share(self):
        '''
        测试了没有权限和正确删除
        '''
        self.client.post('/api/login', {'api_id': '2018000002', 'pwd': '123abc'},
                         content_type='application/json')
        response = self.client.post('/api/manage/share/delete', {'share_id': 2},
                                    content_type='application/json')
        self.assertEqual(response.status_code,403)
        self.client.post('/api/logout')
        self.client.post('/api/login', {'api_id': '2018000001', 'pwd': '123abc'},
                         content_type='application/json')
        response = self.client.post('/api/manage/share/delete', {'share_id': 2},
                                    content_type='application/json')
        self.assertEqual(response.status_code,200)