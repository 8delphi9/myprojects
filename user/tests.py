import json

from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from user.models import User


# Create your tests here.
class Test(APITestCase):
    client = APIClient()

    def setUp(self):
        super_user = User.objects.create_superuser('admin@google.com', 'admin', 'adminpass')
        self.user = super_user

        user = User.objects.create_user('test5@gmail.com','test5','Testtest1@')

        user.save()
        self.user = user
        self.assertIsInstance(user, User)

    def test_signup(self):
        context = {
            'email': 'test2@gmail.com',
            'password1': 'Testtest1@',
            'password2': 'Testtest1@',
            'nickname': 'test2'
        }
        response = self.client.post(
            f'/api/user/signup/',
            json.dumps(context),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

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