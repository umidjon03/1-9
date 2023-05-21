from django.urls import reverse
from rest_framework.test import APITestCase

from users.tests.constants import USER_TOKEN
from tasks.models import Task


class TaskTest(APITestCase):
    fixtures = ('users_and_tokens.yaml', 'tasks_testing.json')

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + USER_TOKEN)

    def test_list(self):
        response = self.client.get(reverse('tasks:my_tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['id'], 1)
        self.assertEqual(response.data['results'][1]['id'], 2)

    def test_create(self):
        response = self.client.post(reverse('tasks:my_tasks'), {
            'firstname': 'Umidjon',
            'task_summary': 'Just Summary',
            'task_context': 'The body of the task',
            'user': 1,
        })
        self.assertEqual(response.status_code, 201)

        response = self.client.post(reverse('tasks:my_tasks'), {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["task_summary"], ["This field is required."])
        self.assertEqual(response.data["task_context"], ["This field is required."])


    def test_detail(self):
        response = self.client.get(reverse('tasks:task_rud', kwargs={"task_id": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['completed'], False)

    def test_delete(self):
        response = self.client.delete(reverse('tasks:task_rud', kwargs={"task_id": 3}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Task.objects.filter(pk=3).exists(), False)

    def test_update(self):
        task_old = Task.objects.get(id=1)
        url = reverse('tasks:task_rud', kwargs={"task_id": 1})
        response = self.client.put(url, {
            'task_summary': 'updated 1 to switch completed to True',
            'completed': True
        })
        task_new = Task.objects.get(id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['task_summary'], 'updated 1 to switch completed to True')
        self.assertEqual(response.data['completed'], True)

        self.assertGreater(task_new.updated, task_old.updated)
