import jwt
import json
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Task
from datetime import datetime, timedelta

class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='testuser1', password='testpassword1')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword2')
        
        # Create sample tasks
        self.task1 = Task.objects.create(user=self.user1, title='Task 1', duration=30)
        self.task2 = Task.objects.create(user=self.user1, title='Task 2', duration=45)
        self.task3 = Task.objects.create(user=self.user2, title='Task 3', duration=60)
        
        # Generate token for user1
        payload = {
            'user_id': self.user1.id,
            'exp': (datetime.now() + timedelta(minutes=5)).timestamp()
        }
        self.token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')

    def test_create_task(self):
        """Test creating a new task"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {'title': 'Test Task', 'duration': 30}
        response = self.client.post(reverse('task-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 4)
        self.assertEqual(Task.objects.get(title='Test Task').title, 'Test Task')

    def test_get_task_list(self):
        """Test getting last 4 tasks"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        # Create more tasks
        for i in range(3):  # Creating 3 more tasks to have total of 6
            Task.objects.create(user=self.user1, title=f'Extra Task {i}', duration=30)

        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # Should only return last 4
        tasks_titles = [task['title'] for task in response.data]
        self.assertTrue(all(f'Extra Task {i}' in tasks_titles for i in range(3)))

    def test_retrieve_task(self):
        """Test retrieving a single task using raw SQL"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(reverse('task-detail', args=[self.task1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Task 1')

    def test_update_task(self):
        """Test updating only the title of a task using raw SQL"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {'title': 'Updated Title', 'duration': 60}
        response = self.client.put(reverse('task-detail', args=[self.task1.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')
        self.assertEqual(response.data['duration'], 30)  # Duration should not change

    def test_delete_task(self):
        """Test deleting own task"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        initial_count = Task.objects.count()
        response = self.client.delete(reverse('task-detail', args=[self.task1.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), initial_count - 1)

    def test_delete_other_user_task(self):
        """Test attempting to delete another user's task"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        initial_count = Task.objects.count()
        response = self.client.delete(reverse('task-detail', args=[self.task3.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Task.objects.count(), initial_count)  # Count should not change

    def test_unauthorized_access(self):
        """Test accessing endpoint without token"""
        self.client.credentials()  # Remove any existing credentials
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_cannot_access_other_users_task(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(reverse('task-detail', kwargs={'pk': self.task3.id}))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)