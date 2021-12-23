from django.urls import reverse
from grades.models import Semester
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

class TestSemester(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # register user
        url = reverse('accounts:register')
        credentials = {'email': 'test@test.com', 'password': 'testpassword123'}
        self.client.post(url, credentials, format='json')
        # gets user token
        url = reverse('accounts:login')
        token_response = self.client.post(url, credentials, format='json')
        # authenticates user
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_response.data['token']}")
        self.url = reverse('grades:semesters')
        self.data = {
            "name": "CICLO 2021-2",
            "order": 8,
            "progress_score": 0.0,
            "target_score": 0.0,
            "total_credits": 0,
            "is_completed": False
        }

    def test_create_semester(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Semester.objects.count(), 1)
        self.assertEqual(Semester.objects.get().name, self.data['name'])
        self.assertEqual(Semester.objects.get().order, self.data['order'])
        self.assertEqual(Semester.objects.get().progress_score, self.data['progress_score'])
        self.assertEqual(Semester.objects.get().target_score, self.data['target_score'])
        self.assertEqual(Semester.objects.get().total_credits, self.data['total_credits'])
        self.assertEqual(Semester.objects.get().is_completed, self.data['is_completed'])
        return response

    def test_list_semester(self):
        self.test_create_semester()
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], self.data['name'])

    def test_retrieve_semester(self):
        semester = self.test_create_semester()
        url = reverse('grades:semester-detail',kwargs={'id': semester.data['id']})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.data['name'])

    def test_update_semester(self):
        semester = self.test_create_semester()
        url = reverse('grades:semester-detail',kwargs={'id': semester.data['id']})
        data = {'number': 2}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.data['name'])

    def test_delete_semester(self):
        semester = self.test_create_semester()
        # deletes semester
        url = reverse('grades:semester-detail',kwargs={'id': semester.data['id']})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Semester.objects.all().count(), 0)
        
class TestCourse(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # register user
        url = reverse('accounts:register')
        credentials = {'email': 'test@test.com', 'password': 'testpassword123'}
        self.client.post(url, credentials, format='json')
        # gets user token
        url = reverse('accounts:login')
        token_response = self.client.post(url, credentials, format='json')
        # authenticates user
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_response.data['token']}")
        self.url = reverse('grades:semesters')
        self.data = {
            "name": "CICLO 2021-2",
            "term": 8,
            "progress_score": 0.0,
            "target_score": 0.0,
            "total_credits": 0,
            "is_completed": False
        }