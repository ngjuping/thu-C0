from mongoengine import connect, disconnect
from Qinghuiyue.users.models import User
from Qinghuiyue.models.models import Stat
from Qinghuiyue.test import NoSQLTestCase


class UserViewTest(NoSQLTestCase):

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
        User.create(password='123abc', user_id=Stat.add_object("user"), name='test',
                    api_id='2018000001', privilege=0)

    @classmethod
    def tearDownClass(cls):
        '''
        断开假服务器，数据不会保存
        '''
        disconnect()

    def test_signup(self):
        # 成功注册
        response = self.client.post('/api/signup', {'api_id': '2018000000', 'name': '清会约', 'pwd': '123abc'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # 失败
        response = self.client.post('/api/signup', {'api_id': '2018000000', 'name': '清会约', 'pwd': '123abc'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 403)
        response = self.client.post('/api/signup', {'api_id': '20180000000', 'name': '清会约', 'pwd': '123abc'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        #成功
        response = self.client.post('/api/login', {'api_id': '2018000001', 'pwd': '123abc'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        #失败
        response = self.client.post('/api/login', {'api_id': '2018000001', 'pwd': '123abcd'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_logout(self):
        self.client.post('/api/login', {'api_id': '2018000001', 'pwd': '123abc'},
                                    content_type='application/json')
        response=self.client.post('/api/logout')
        self.assertEqual(response.status_code,200)
    def test_get_name_by_id(self):
        response=self.client.get('/api/manage/getuserids?user_name=清')
        self.assertEqual(response.status_code,200)
