from mongoengine import connect, disconnect
from Qinghuiyue.models.models import Stat
from Qinghuiyue.models.models import Course
from Qinghuiyue.test import NoSQLTestCase
from Qinghuiyue.users.models import *


class AdminCourseViewTest(NoSQLTestCase):

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
        Course.objects.create(course_id=1,name='Jijian class',price='20 dollar',tel= '13146055588',intro='a class for jijianing')
        Course.objects.create(course_id=2,name='Jijian class', price='20 dollar', tel='13146055588', intro='a class for jijianing')
        Course.objects.create(course_id=3, name='Jijian class', price='20 dollar', tel='13146055588',
                              intro='a class for jijianing')
        User.create(password='123abc', user_id=1, name='test',api_id='2018000000', privilege=1)

    @classmethod
    def tearDownClass(cls):
        '''
        断开假服务器，数据不会保存
        '''
        disconnect()

    def test_create_class(self):
        self.client.post('/api/login', {'api_id':'2018000000', 'pwd':'123abc'},content_type='application/json')
        # 成功
        response = self.client.post('/api/admin/create/course',
                                    {'name': 'Jiclass',
                                     'price': '20 dollar',
                                     'tel': '13146055588',
                                     'intro': 'a class for jijianing'
                                    },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # 失败
        response = self.client.post('/api/admin/create/course',
                                    {'name': 'Jijian class',
                                     'price': '20 dollar',
                                     'tel': '13146055588',
                                     'intro': 'a class for jijianing'
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        response = self.client.post('/api/admin/create/course',
                                    {'name': 'Jiclass',
                                     'price': '20 dollar',
                                     'tel': '10',
                                     'intro': 'a class for jijianing'
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        response = self.client.post('/api/admin/create/course',
                                    {'name': 'Ji',
                                     'price': '20 dollar',
                                     'tel': '13146055588',
                                     'intro': 'a class for jijianing'
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        response = self.client.post('/api/admin/create/course',
                                    {'name': 'Jiclass',
                                     'price': '20 dollar',
                                     'tel': '13146055588'*3,
                                     'intro': 'a class for jijianing'
                                    },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        response = self.client.post('/api/admin/create/course',
                                    {'name': 'Jiclass',
                                     'price': '20 dollar',
                                     'tel': '13146055588',
                                     'intro': 'a class for jijianing'*30
                                    },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        response = self.client.post('/api/admin/create/course',
                                    {'name': 'Jiclass',
                                     'price': '',
                                     'tel': '13146055588',
                                     'intro': 'a class for jijianing'
                                    },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_update_class(self):
        self.client.post('/api/login', {'api_id': '2018000000', 'pwd': '123abc'}, content_type='application/json')
        # 成功
        response = self.client.post('/api/admin/update/course',
                                    {'course_id': 2,
                                     'name': "badclass"
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/api/admin/update/course',
                                    {'course_id': 2,
                                     'tel': "13344555544"
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/api/admin/update/course',
                                    {'course_id': 2,
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # 失败
        response = self.client.post('/api/admin/update/course',
                                    {'course_id': 2,
                                     'name': 'Jijian class',
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        response = self.client.post('/api/admin/update/course',
                                    {'course_id': 2,
                                     'tel': '10',
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        response = self.client.post('/api/admin/update/course',
                                    {'name': 'Ji',
                                     'course_id': 2,
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        response = self.client.post('/api/admin/update/course',
                                    {'course_id': 2,
                                     'tel': '13146055588' * 3,
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        response = self.client.post('/api/admin/update/course',
                                    {'course_id': 2,
                                     'intro': 'a class for jijianing' * 30
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        response = self.client.post('/api/admin/update/course',
                                    {'course_id': 2,
                                     'price': '',
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_delete_class(self):
        self.client.post('/api/login', {'api_id': '2018000000', 'pwd': '123abc'}, content_type='application/json')
        response = self.client.post('/api/admin/delete/course',
                                    {'course_id': 4,
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

        # 成功
        response = self.client.post('/api/admin/delete/course',
                                    {'course_id': 1,
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # 失败
        response = self.client.post('/api/admin/delete/course',
                                    {'course_id': 1,
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_get_class(self):
        self.client.post('/api/login', {'api_id': '2018000000', 'pwd': '123abc'}, content_type='application/json')
        response = self.client.get('/api/courses?page=1&size=5',

                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/courses?page=1',

                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

        response = self.client.get('/api/courses?size=5',

                                   content_type='application/json')
        self.assertEqual(response.status_code, 401)
