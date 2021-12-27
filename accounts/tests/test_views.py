from django.core import mail
from django.test.utils import modify_settings, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from accounts.models import User


class TestRegisterViews(APITestCase):

    @classmethod
    def setUp(self):
        self.client = APIClient()
        self.credentials = {
            "email": "test@test.com",
            "password": "testpassword123"
        }

    def test_register_view_post(self):
        url = reverse('accounts:register')
        response = self.client.post(url, self.credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(len(mail.outbox), 1)

    def test_register_view_exception(self):
        url = reverse('accounts:register')
        credentials = {
            "email": "test@test.com",
            "password": ""
        }
        response = self.client.post(url, credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(len(mail.outbox), 0)

    def test_register_view_no_email_exception(self):
        credentials = {
            "password": "testpassword123"
        }
        url = reverse('accounts:register')
        response = self.client.post(url, credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(len(mail.outbox), 0)

    def test_register_view_no_password_exception(self):
        credentials = {
            "email": "test@test.com"
        }
        url = reverse('accounts:register')
        response = self.client.post(url, credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(len(mail.outbox), 0)

    def test_register_view_bad_email_exception(self):
        credentials = {
            "email": "bademail",
            "password": "testpassword123"
        }
        url = reverse('accounts:register')
        response = self.client.post(url, credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(len(mail.outbox), 0)

    def test_register_view_bad_password_exception(self):
        credentials = {
            "email": "test@test.com",
            "password": ""
        }
        url = reverse('accounts:register')
        response = self.client.post(url, credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(len(mail.outbox), 0)


class TestActivationViews(APITestCase):
    @classmethod
    def setUp(self):
        self.client = APIClient()
        self.credentials = {
            "email": "test@test.com",
            "password": "testpassword123"
        }

    def test_activation_put(self):
        url = reverse('accounts:register')
        response = self.client.post(url, self.credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        emailtoken = mail.outbox[0].body.split('/activate/')[1]
        response = self.client.put(
            reverse('accounts:activate', kwargs={'token': emailtoken}))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_activation_put_bad_request(self):
        response = self.client.put(
            reverse('accounts:activate', kwargs={'token': 'badtoken'}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Token is invalid")


class TestLoginViews(APITestCase):
    @classmethod
    def setUp(self):
        self.client = APIClient()
        self.credentials = {
            "email": "test@test.com",
            "password": "testpassword123"
        }
        # Register:
        url = reverse('accounts:register')
        self.client.post(url, self.credentials, format='json')
        # Activation:
        emailtoken = mail.outbox[0].body.split('/activate/')[1]
        self.client.put(reverse('accounts:activate',
                        kwargs={'token': emailtoken}))
        self.url = reverse('accounts:login')

    def test_login_view_post(self):
        response = self.client.post(self.url, self.credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_view_post_bad_request(self):
        self.credentials = {
            "email": "test@test.com",
            "password": "badpassword"
        }
        response = self.client.post(self.url, self.credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestUserAuthViews(APITestCase):
    @classmethod
    def setUp(self):
        self.client = APIClient()
        self.user = {
            "email": "test@test.com",
            "password": "testpassword123"
        }
        # Register:
        url = reverse('accounts:register')
        self.client.post(url, self.user, format='json')
        # Activation:
        emailtoken = mail.outbox[0].body.split('/activate/')[1]
        self.client.put(reverse('accounts:activate',
                        kwargs={'token': emailtoken}))
        token_response = self.client.post(
            reverse('accounts:login'), self.user, format='json')
        self.auth_headers = {
            'HTTP_AUTHORIZATION': f"Bearer {token_response.data['token']}",
        }

    def test_user_auth_view_get(self):
        response = self.client.get(
            reverse('accounts:auth-user'), format='json', **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user['email'])

    def test_user_auth_view_get_aux(self):
        auth_headers = {
            'HTTP_AUTHORIZATION': "badtoken",
        }
        response = self.client.get(
            reverse('accounts:auth-user'), format='json', **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestUserDetailViews(APITestCase):
    @classmethod
    def setUp(self):
        self.client = APIClient()
        self.user = {
            "email": "test@test.com",
            "password": "testpassword123"
        }
        # Register:
        url = reverse('accounts:register')
        self.client.post(url, self.user, format='json')
        self.userobj = User.objects.get(email=self.user['email'])
        self.userobj.is_staff = True
        self.userobj.save()
        # Activation:
        emailtoken = mail.outbox[0].body.split('/activate/')[1]
        self.client.put(reverse('accounts:activate',
                        kwargs={'token': emailtoken}))
        token_response = self.client.post(
            reverse('accounts:login'), self.user, format='json')
        self.auth_headers = {
            'HTTP_AUTHORIZATION': f"Bearer {token_response.data['token']}",
        }
        # We retrieve the created user:

    def test_user_detail_view_get_queryset(self):
        response = self.client.get(reverse(
            'accounts:user-detail', kwargs={'id': self.userobj.id}), format='json', **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user['email'])


class TestUserListViews(APITestCase):
    @classmethod
    def setUp(self):
        self.client = APIClient()
        self.user = {
            "email": "test@test.com",
            "password": "testpassword123"
        }
        # Register:
        url = reverse('accounts:register')
        self.client.post(url, self.user, format='json')
        self.userobj = User.objects.get(email=self.user['email'])
        self.userobj.is_staff = True
        self.userobj.save()
        # Activation:
        emailtoken = mail.outbox[0].body.split('/activate/')[1]
        self.client.put(reverse('accounts:activate',
                        kwargs={'token': emailtoken}))
        token_response = self.client.post(
            reverse('accounts:login'), self.user, format='json')
        self.auth_headers = {
            'HTTP_AUTHORIZATION': f"Bearer {token_response.data['token']}",
        }
        # We retrieve the created user:

    def test_user_list_view_get_queryset(self):
        response = self.client.get(
            reverse('accounts:users'), format='json', **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], self.user['email'])
