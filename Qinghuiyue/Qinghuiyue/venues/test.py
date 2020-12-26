from mongoengine import connect, disconnect
from Qinghuiyue.models.models import Stat
from Qinghuiyue.models.models import Notification
from Qinghuiyue.test import NoSQLTestCase
from Qinghuiyue.venues.models import *
from django.core.files.uploadedfile import SimpleUploadedFile


class AdminNoticeViewTest(NoSQLTestCase):

    @classmethod
    def setUpClass(cls):
        '''
        在该函数中定义需要用到的模型，必须要先disconnect然后连接mock.之后的
        定义要多少自己定
        '''
        disconnect()
        connect('mongoenginetest', host='mongomock://localhost')
        Stat.objects.create(name='size_of_collection', data={'user': 0, 'venue': 0,
                                                             'court': 0, 'feedback': 0,
                                                             'notification': 0, 'share_notification': 0,
                                                             'reservation': 0, 'course': 0})
        Venue.objects.create(name='name', description='description', img=None, venue_id=1)
        Court.objects.create(name='name', court_id=1)


    @classmethod
    def tearDownClass(cls):
        '''
        断开假服务器，数据不会保存
        '''
        disconnect()


    def test_get_venue(self):
        # 成功
        response = self.client.get('/api/main/venues?id=1')
        self.assertEqual(response.status_code, 200)
        # 失败
        response = self.client.get('/api/main/venues?id=2')
        self.assertEqual(response.status_code, 401)

    def test_list_venue(self):
        # 不需要参数
        response = self.client.get('/api/main/venues/list')
        self.assertEqual(response.status_code, 200)

    def test_booking(self):
        # 存在
        response = self.client.get('/api/booking?id=1')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/booking?id=1&year=2020&month=12&day=21')
        self.assertEqual(response.status_code, 200)

        # 不存在
        response = self.client.get('/api/booking?id=2')
        self.assertEqual(response.status_code, 400)











