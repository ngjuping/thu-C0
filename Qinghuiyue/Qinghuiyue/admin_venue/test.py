from mongoengine import connect, disconnect
from Qinghuiyue.models.models import Stat
from Qinghuiyue.models.models import Notification
from Qinghuiyue.test import NoSQLTestCase
from Qinghuiyue.venues.models import *
from django.core.files.uploadedfile import SimpleUploadedFile
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
        Venue.objects.create(name='name', description='description', img=None, venue_id=1)
        Court.objects.create(name='name', court_id=1,venue_id=1)
        User.create(password='123abc', user_id=1, name='test', api_id='2018000000', privilege=1)
        Court.objects.create(name='name', court_id=2, venue_id=1)

    @classmethod
    def tearDownClass(cls):
        '''
        断开假服务器，数据不会保存
        '''
        disconnect()


    def test_create_venue(self):
        self.client.post('/api/login', {'api_id': '2018000000', 'pwd': '123abc'}, content_type='application/json')
        # 成功
        response = self.client.post('/api/admin/create/venue',
                                    {'name': 'name',
                                     'description': 'description',
                                     'img': SimpleUploadedFile(name='test_image.jpg', content=open('C:/Users/pb/Pictures/birdhouse.jpg', 'rb').read(),
                                                        content_type='image/jpg')
                                     },
                                    )
        self.assertEqual(response.status_code, 200)
        # 失败
        response = self.client.post('/api/admin/create/venue',
                                    {'name': 'na',
                                     'description': 'description',
                                     'img': SimpleUploadedFile(name='test_image.jpg',
                                                               content=open('C:/Users/pb/Pictures/birdhouse.jpg',
                                                                            'rb').read(),
                                                               content_type='image/jpg')
                                     },
                                    )
        self.assertEqual(response.status_code, 401)
        response = self.client.post('/api/admin/create/venue',
                                    {'name': 'name',
                                     'description': 'd',
                                     'img': SimpleUploadedFile(name='test_image.jpg',
                                                               content=open('C:/Users/pb/Pictures/birdhouse.jpg',
                                                                            'rb').read(),
                                                               content_type='image/jpg')
                                     },
                                    )
        self.assertEqual(response.status_code, 401)
        response = self.client.post('/api/admin/create/venue',
                                    {'name': 'name',
                                     'description': 'description',
                                     },
                                    )
        self.assertEqual(response.status_code, 401)

    def test_create_court(self):
        self.client.post('/api/login', {'api_id': '2018000000', 'pwd': '123abc'}, content_type='application/json')
        # 成功
        response = self.client.post('/api/admin/create/court',
                                    {'name': 'name',
                                     'venue_id': 1,
                                     'type': 1,
                                     'price': 15,
                                     'status': [
                                         {
                                             "start": "2020-11-26T16:00:00+00:00",
                                             "end": "2020-11-26T17:00:00+00:00",
                                             "code": 1
                                         }
                                     ]
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # 失败
        response = self.client.post('/api/admin/create/court',
                                    {'name': 'na',
                                     'venue_id': 1,
                                     'type': 1,
                                     'price': 15,
                                     'status': [
                                         {
                                             "start": "2020-11-26T16:00:00+00:00",
                                             "end": "2020-11-26T17:00:00+00:00",
                                             "code": 1
                                         }
                                     ]
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

        response = self.client.post('/api/admin/create/court',
                                    {'name': 'name'*10,
                                     'venue_id': 1,
                                     'type': 1,
                                     'price': 15,
                                     'status': [
                                         {
                                             "start": "2020-11-26T16:00:00+00:00",
                                             "end": "2020-11-26T17:00:00+00:00",
                                             "code": 1
                                         }
                                     ]
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

        response = self.client.post('/api/admin/create/court',
                                    {'name': 'name',
                                     'type': 1,
                                     'price': 15,
                                     'status': [
                                         {
                                             "start": "2020-11-26T16:00:00+00:00",
                                             "end": "2020-11-26T17:00:00+00:00",
                                             "code": 1
                                         }
                                     ]
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

        response = self.client.post('/api/admin/create/court',
                                    {'name': 'name',
                                     'venue_id': 1,
                                     'type': '1',
                                     'price': 15,
                                     'status': [
                                         {
                                             "start": "2020-11-26T16:00:00+00:00",
                                             "end": "2020-11-26T17:00:00+00:00",
                                             "code": 1
                                         }
                                     ]
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

        response = self.client.post('/api/admin/create/court',
                                    {'name': 'name',
                                     'venue_id': 1,
                                     'type': 1,
                                     'price': '15',
                                     'status': [
                                         {
                                             "start": "2020-11-26T16:00:00+00:00",
                                             "end": "2020-11-26T17:00:00+00:00",
                                             "code": 1
                                         }
                                     ]
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

        response = self.client.post('/api/admin/create/court',
                                    {'name': 'name',
                                     'venue_id': 1,
                                     'type': 1,
                                     'price': 15,
                                     'status': [
                                         {
                                             "code": 1
                                         }
                                     ]
                                     },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_update_venue(self):
        self.client.post('/api/login', {'api_id': '2018000000', 'pwd': '123abc'}, content_type='application/json')
        # 成功
        response = self.client.post('/api/admin/update/venue',
                                    {'name': 'name',
                                     'venue_id': 1,
                                     'description': 'description',
                                     'img': SimpleUploadedFile(name='test_image.jpg', content=open('C:/Users/pb/Pictures/birdhouse.jpg', 'rb').read(),
                                                        content_type='image/jpg')
                                     },
                                    )
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/api/admin/update/venue',
                                    {
                                     'venue_id': 1,
                                     'img': SimpleUploadedFile(name='test_image.jpg',
                                                               content=open('C:/Users/pb/Pictures/birdhouse.jpg',
                                                                            'rb').read(),
                                                               content_type='image/jpg')
                                     },
                                    )
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/api/admin/update/venue',
                                    {'name': 'name',
                                     'venue_id': 1,
                                     'description': 'description',
                                     },
                                    )
        self.assertEqual(response.status_code, 200)

        # 失败

        response = self.client.post('/api/admin/update/venue',
                                    {'name': 'name',
                                     'description': 'description',
                                     'img': SimpleUploadedFile(name='test_image.jpg',
                                                               content=open('C:/Users/pb/Pictures/birdhouse.jpg',
                                                                            'rb').read(),
                                                               content_type='image/jpg')
                                     },
                                    )
        self.assertEqual(response.status_code, 401)

    def test_delete_venue(self):
        self.client.post('/api/login', {'api_id': '2018000000', 'pwd': '123abc'}, content_type='application/json')
        response = self.client.post('/api/admin/delete/venue',
                                    {
                                        'venue_id': 3
                                    },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

        response = self.client.post('/api/admin/delete/venue',
                                {
                                    'venue_id':1
                                },
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/api/admin/delete/venue',
                                    {
                                        'venue_id': 1
                                    },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_delete_venue(self):
        self.client.post('/api/login', {'api_id': '2018000000', 'pwd': '123abc'}, content_type='application/json')
        response = self.client.post('/api/admin/delete/court',
                                    {
                                        'court_id': 3
                                    },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

        response = self.client.post('/api/admin/delete/court',
                                {
                                    'court_id':1
                                },
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/api/admin/delete/court',
                                    {
                                        'court_id': 1
                                    },
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_list_court(self):
        self.client.post('/api/login', {'api_id': '2018000000', 'pwd': '123abc'}, content_type='application/json')

        response = self.client.get('/api/admin/court/list?page=1',

                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

        response = self.client.get('/api/admin/court/list?size=5',

                                   content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_make_schedule(self):
        submatrix = [1,1,1,1,1,1,1]
        matrix = []
        for i in range(15):
            matrix.append(submatrix)

        response = self.client.post('/api/admin/schedule',{
            'court_id':2,
            'price':15,
            'matrix': matrix
        }
        ,content_type='application/json')
        self.assertEqual(response.status_code, 403)

        self.client.post('/api/login', {'api_id': '2018000000', 'pwd': '123abc'}, content_type='application/json')

        response = self.client.post('/api/admin/schedule', {
            'court_id': 2,
            'price': 15,
            'matrix': matrix
        }
                                    , content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/api/admin/schedule', {
            'court_id': 10,
            'price': 15,
            'matrix': matrix
        }
                                    , content_type='application/json')
        self.assertEqual(response.status_code, 501)





    def generate_csv(self):
        self.client.post('/api/login', {'api_id': '2018000000', 'pwd': '123abc'}, content_type='application/json')
        response = self.client.get('/api/admin/csv/generate',

                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)







