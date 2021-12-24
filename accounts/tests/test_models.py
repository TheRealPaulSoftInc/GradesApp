from rest_framework.test import APITestCase
from accounts.models import User

class TestUserModelManager(APITestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@test.com', password='testpassword123')
        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email, 'test@test.com')

    def test_error_create_user_no_password(self):
        with self.assertRaisesMessage(ValueError, 'The Password must be set'):
            User.objects.create_user(email='test@test.com', password='')

    def test_error_create_user_no_email(self):
        with self.assertRaisesMessage(ValueError, 'The Email must be set'):
            User.objects.create_user(email='', password='testpassword123')

    def test_create_user_token(self):
        user = User.objects.create_user(
            email='test@test.com', password='testpassword123')
        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email, 'test@test.com')
        token = user.token
        #We verify the token by his str length
        self.assertIsInstance(token, str)
        self.assertTrue(len(token)>0)

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email='test@test.com', password='testpassword123')
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.email, 'test@test.com')

    def test_create_superuser_no_password(self):
        with self.assertRaisesMessage(ValueError, 'The Password must be set'):
            User.objects.create_superuser(email='test@test.com', password='')

    def test_create_superuser_no_email(self):
        with self.assertRaisesMessage(ValueError, 'The Email must be set'):
            User.objects.create_superuser(email='', password='testpassword123')

    def test_error_create_superuser_is_not_staff(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_staff=True.'):
            user = User.objects.create_superuser(
                email='test@test.com', password='testpassword123', is_staff=False)

    def test_error_create_superuser_is_not_superuser(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_superuser=True.'):
            user = User.objects.create_superuser(
                email='test@test.com', password='testpassword123',is_staff=True, is_superuser=False)

    def test_user_get_str(self):
        user = User.objects.create_user(
            email='test@test.com', password='testpassword123')
        self.assertEqual(user.__str__(), 'test@test.com')