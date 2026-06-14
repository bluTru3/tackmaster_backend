from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task

class TaskModelTest(TestCase):
    def test_create_task(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        task = Task.objects.create(
            user=user,
            title='Test Task',
            description='Test Description'
        )
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(str(task), 'Test Task')

class AuthAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/register/'
        self.login_url = '/api/login/'
    
    def test_user_registration(self):
        data = {'username': 'newuser', 'password': 'newpass123'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_user_login(self):
        User.objects.create_user(username='testuser', password='testpass')
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

class TaskAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='taskuser', password='taskpass')
        response = self.client.post('/api/login/', 
            {'username': 'taskuser', 'password': 'taskpass'}, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    def test_create_task(self):
        data = {'title': 'API Task', 'description': 'Created via test'}
        response = self.client.post('/api/tasks/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
    
    def test_list_tasks(self):
        Task.objects.create(user=self.user, title='Task 1')
        Task.objects.create(user=self.user, title='Task 2')
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

