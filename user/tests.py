import json

from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from user.models import User


# Create your tests here.
class UserTest(APITestCase):
    client = APIClient()
    headers = {}

    def setUp(self):
        # superuser
        super_user = User.objects.create_superuser(
            email='admin@google.com',
            nickname='admin_test',
            password='adminpass'
        )
        super_user.save()
        self.admin = super_user

        user = User.objects.create_user('test5@gmail.com', 'test5', 'Testtest1@')

        user.save()
        self.user = user
        self.assertIsInstance(user, User)

        # herders
        data = {
            'email': 'admin@google.com',
            'password': 'adminpass'
        }
        response = self.client.post('/api/user/login/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        self.token_access = response.data['token']['access']
        self.assertNotEqual(self.token_access, '')

        self.headers = {
            'HTTP_Authorization': 'Bearer ' + self.token_access,
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_access}')

    def test_user_update(self):
        login_context = {
            'email': 'test5@gmail.com',
            'password': 'Testtest1@'
        }
        response = self.client.post(
            f'/api/user/login/',
            json.dumps(login_context),
            content_type='application/json'
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["token"]["access"]}')

        context = {
            'email': response.data['email'],
            'nickname': 'test55'
        }
        response = self.client.patch(
            f'/api/user/',
            json.dumps(context),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)

    def test_user_delete(self):
        login_context = {
            'email': 'test5@gmail.com',
            'password': 'Testtest1@'
        }
        response = self.client.post(
            f'/api/user/login/',
            json.dumps(login_context),
            content_type='application/json'
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["token"]["access"]}')

        context = {
            'email': response.data['email'],
        }
        response = self.client.delete(
            f'/api/user/',
            json.dumps(context),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)

    ###### Test Login ######
    def test_success_admin_login(self):
        user = {
            'email': 'admin@google.com',
            'password': 'adminpass'
        }

        response = self.client.post('/api/user/login/', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_fail_admin_login(self):
        user = {
            'email': 'admin@google.com',
            'password': 'fallpassword'
        }

        response = self.client.post('/api/user/login/', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_success_user_login(self):
        user = {
            'email': 'test5@gmail.com',
            'password': 'Testtest1@'
        }

        response = self.client.post('/api/user/login/', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_fail_user_login(self):
        user = {
            'email': 'test5@gmail.com',
            'password': 'Test'
        }

        response = self.client.post('/api/user/login/', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_token_login(self):
        user = {
            'email': 'admin@google.com',
            'password': 'adminpass'
        }

        response = self.client.post('/api/user/login/', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        self.token_access = response.data['token']['access']
        self.token_refresh = response.data['token']['refresh']
        self.assertNotEqual(self.token_access, '')
        self.assertNotEqual(self.token_refresh, '')

    ##### 어드민전용 #####
    def test_read_success_admin(self):
        response = self.client.get('/api/admin/user/', **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_read_fail_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='')

        response = self.client.get('/api/admin/user/', **self.headers, content_type='application/json')
        self.assertEqual(response.status_code, 401)






