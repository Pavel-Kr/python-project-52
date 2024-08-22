from django.test import Client, TestCase
from django.urls import reverse

from tasks.models import Task


def login_test_user(client: Client):
    credentials = {
        'username': 'test_user',
        'password': 'password'
    }
    client.login(**credentials)


def build_login_url(next):
    return f'{reverse("users:login")}?next={next}'


class TasksTestCase(TestCase):
    fixtures = ['users.json', 'tasks.json', 'statuses.json']

    def test_read_tasks(self):
        login_test_user(self.client)

        tasks_url = reverse('tasks:index')
        response = self.client.get(tasks_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test task 1')
        self.assertContains(response, 'Test task 2')

    def test_read_tasks_unauth(self):
        tasks_url = reverse('tasks:index')
        redir_url = build_login_url(tasks_url)
        response = self.client.get(tasks_url, follow=True)

        # Check login redirect
        self.assertRedirects(response, redir_url)
        self.assertContains(response, 'alert-danger')

    def test_create_task(self):
        login_test_user(self.client)

        task = {
            'name': 'Test create',
            'description': 'Test of task creation',
            'status': 1,
        }

        create_url = reverse('tasks:create')
        redir_url = reverse('tasks:index')
        response = self.client.post(create_url, task, follow=True)
        self.assertRedirects(response, redir_url)
        self.assertContains(response, 'alert-success')

        # Check that task has been created
        db_entry = Task.objects.get(name='Test create')
        self.assertIsNotNone(db_entry)

    def test_create_task_unauth(self):
        create_url = reverse('tasks:create')
        redir_url = build_login_url(create_url)
        task = {
            'name': 'Test create',
            'description': 'Test of task creation',
            'status': 1,
        }
        response = self.client.post(create_url,
                                    task,
                                    follow=True)

        # Check login redirect
        self.assertRedirects(response, redir_url)
        self.assertContains(response, 'alert-danger')

    def test_update_task(self):
        login_test_user(self.client)

        update_task = {
            'name': 'Test update',
            'description': 'Testing task update',
            'performer': 4,
            'status': 2,
            'author': 3
        }

        update_url = reverse('tasks:update', kwargs={'pk': 3})
        redir_url = reverse('tasks:index')
        response = self.client.post(update_url, data=update_task, follow=True)

        self.assertRedirects(response, redir_url)
        self.assertContains(response, 'alert-success')

        # Check that task has been updated
        db_entry = Task.objects.get(pk=3)
        self.assertEqual(db_entry.name, 'Test update')
        self.assertEqual(db_entry.description, 'Testing task update')

    def test_task_update_unauth(self):
        update_task = {
            'name': 'Test update',
            'description': 'Testing task update',
            'performer': 4,
            'status': 2,
            'author': 3
        }

        update_url = reverse('tasks:update', kwargs={'pk': 3})
        redir_url = build_login_url(update_url)
        response = self.client.post(update_url, data=update_task, follow=True)

        self.assertRedirects(response, redir_url)
        self.assertContains(response, 'alert-danger')

    def test_task_delete(self):
        login_test_user(self.client)

        delete_url = reverse('tasks:delete', kwargs={'pk': 1})
        redir_url = reverse('tasks:index')

        response = self.client.post(delete_url, follow=True)

        self.assertRedirects(response, redir_url)
        self.assertContains(response, 'alert-success')

        # Check that task has been deleted
        with self.assertRaisesMessage(Task.DoesNotExist,
                                      'does not exist'):
            Task.objects.get(pk=1)

    def test_task_delete_unauth(self):
        delete_url = reverse('tasks:delete', kwargs={'pk': 1})
        redir_url = build_login_url(delete_url)

        response = self.client.post(delete_url, follow=True)

        self.assertRedirects(response, redir_url)
        self.assertContains(response, 'alert-danger')

    def test_task_delete_wrong_user(self):
        login_test_user(self.client)

        # Task 3 was created by another author, should not delete
        delete_url = reverse('tasks:delete', kwargs={'pk': 3})
        redir_url = reverse('tasks:index')

        response = self.client.post(delete_url, follow=True)

        self.assertRedirects(response, redir_url)
        self.assertContains(response, 'alert-danger')

        # Check that entry was not deleted
        db_entry = Task.objects.get(pk=3)
        self.assertIsNotNone(db_entry)
