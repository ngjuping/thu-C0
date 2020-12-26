from mongoengine import connect, disconnect
from Qinghuiyue.models.models import Stat
from Qinghuiyue.models.models import Notification
from Qinghuiyue.test import NoSQLTestCase
from datetime import datetime
from Qinghuiyue.users.models import *


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
        Notification.objects.create(name='tongzhi', content='i am coming', time=datetime.now(), notice_id=1)
        User.create(password='123abc', user_id=1, name='test', api_id='2018000000', privilege=1)
    @classmethod
    def tearDownClass(cls):
        '''
        断开假服务器，数据不会保存
        '''
        disconnect()

    def test_create_notice(self):
        self.client.post('/api/login', {'api_id': '2018000000', 'pwd': '123abc'}, content_type='application/json')
        # 成功
        response = self.client.post('/api/admin/create/notice',
                                    {'title': 'title',
                                     'content': 'content',
                                    },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # 失败
        response = self.client.post('/api/admin/create/notice',
									{'content': 'content',
									 },
									content_type='application/json')
        self.assertEqual(response.status_code, 401)

        response = self.client.post('/api/admin/create/notice',
									{'title': 'title'*3,
									 'content': 'content',
									 },
									content_type='application/json')
        self.assertEqual(response.status_code, 401)

        response = self.client.post('/api/admin/create/notice',
									{'title': 'title',
									 'content': 'content'*50,
									 },
									content_type='application/json')
        self.assertEqual(response.status_code, 401)

        response = self.client.post('/api/admin/create/notice',
									{'title': 'title'*3,
									 'content': 'content',
									 },
									content_type='application/json')
        self.assertEqual(response.status_code, 401)

        response = self.client.post('/api/admin/create/notice',
                                    {'title': 'title',
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_update_notice(self):
        self.client.post('/api/login', {'api_id': '2018000000', 'pwd': '123abc'}, content_type='application/json')
        # 成功
        response = self.client.post('/api/admin/update/notice',
                                    {'notice_id': 1,
                                     'title': 'title',
                                     'content': 'content',
                                    },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # 失败
        response = self.client.post('/api/admin/update/notice',
									{'title': 'title',
									 'content': 'content'*50,
                                     'notice_id':1
									 },
									content_type='application/json')
        self.assertEqual(response.status_code, 401)

        response = self.client.post('/api/admin/update/notice',
									{'title': 'title'*3,
                                     'notice_id': 1,
									 'content': 'content',
									 },
									content_type='application/json')
        self.assertEqual(response.status_code, 401)

        response = self.client.post('/api/admin/update/notice',
                                    {'title': 'title',
                                     'content': 'content',
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)


    def test_delete_notice(self):
        self.client.post('/api/login', {'api_id': '2018000000', 'pwd': '123abc'}, content_type='application/json')
        response = self.client.post('/api/admin/delete/notice',
                                    {'notice_id': 4,
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

        # 成功
        response = self.client.post('/api/admin/delete/notice',
                                    {'notice_id': 1,
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # 失败
        response = self.client.post('/api/admin/delete/notice',
                                    {'notice_id': 1,
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_get_notice(self):
        self.client.post('/api/login', {'api_id': '2018000000', 'pwd': '123abc'}, content_type='application/json')
        response = self.client.get('/api/notices?page=1&size=5',

                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/notices?page=1',

                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

        response = self.client.get('/api/notices?size=5',

                                   content_type='application/json')
        self.assertEqual(response.status_code, 401)




