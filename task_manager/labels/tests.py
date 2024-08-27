from django.test import Client, TestCase
from django.urls import reverse

from .models import Label


def login_test_user(client: Client):
    credentials = {
        'username': 'test_user',
        'password': 'password'
    }
    client.login(**credentials)


def build_login_url(next):
    return f'{reverse("login")}?next={next}'


class TasksTestCase(TestCase):
    fixtures = [
        'users.json',
        'tasks.json',
        'labels.json',
        'statuses.json',
        'ltc.json'
    ]

    def test_read_labels(self):
        login_test_user(self.client)

        labels_url = reverse('labels:index')
        response = self.client.get(labels_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test label 1')
        self.assertContains(response, 'Test label 2')
        self.assertContains(response, 'Test label 3')

    def test_read_labels_unauth(self):
        tasks_url = reverse('labels:index')
        redir_url = build_login_url(tasks_url)
        response = self.client.get(tasks_url, follow=True)

        # Check login redirect
        self.assertRedirects(response, redir_url)
        self.assertContains(response, 'alert-danger')

    def test_create_label(self):
        login_test_user(self.client)

        label = {
            'name': 'Test create label'
        }

        create_url = reverse('labels:create')
        redir_url = reverse('labels:index')
        response = self.client.post(create_url, label, follow=True)
        self.assertRedirects(response, redir_url)
        self.assertContains(response, 'alert-success')

        # Check that label has been created
        db_entry = Label.objects.get(name='Test create label')
        self.assertIsNotNone(db_entry)

    def test_create_label_unauth(self):
        create_url = reverse('labels:create')
        redir_url = build_login_url(create_url)
        label = {
            'name': 'Test create label'
        }
        response = self.client.post(create_url,
                                    label,
                                    follow=True)

        # Check login redirect
        self.assertRedirects(response, redir_url)
        self.assertContains(response, 'alert-danger')

    def test_update_label(self):
        login_test_user(self.client)

        update_label = {
            'name': 'Test update label'
        }

        update_url = reverse('labels:update', kwargs={'pk': 1})
        redir_url = reverse('labels:index')
        response = self.client.post(update_url, data=update_label, follow=True)

        self.assertRedirects(response, redir_url)
        self.assertContains(response, 'alert-success')

        # Check that label has been updated
        db_entry = Label.objects.get(pk=1)
        self.assertEqual(db_entry.name, 'Test update label')

    def test_label_update_unauth(self):
        update_label: dict[str, str] = {
            'name': 'Test update label'
        }

        update_url = reverse('labels:update', kwargs={'pk': 1})
        redir_url = build_login_url(update_url)
        response = self.client.post(update_url, data=update_label, follow=True)

        self.assertRedirects(response, redir_url)
        self.assertContains(response, 'alert-danger')

    def test_label_delete(self):
        login_test_user(self.client)

        # Label 3 is not associated with any task, should delete
        delete_url = reverse('labels:delete', kwargs={'pk': 3})
        redir_url = reverse('labels:index')

        response = self.client.post(delete_url, follow=True)

        self.assertRedirects(response, redir_url)
        self.assertContains(response, 'alert-success')

        # Check that label has been deleted
        with self.assertRaisesMessage(Label.DoesNotExist,
                                      'does not exist'):
            Label.objects.get(pk=3)

    def test_label_delete_unauth(self):
        delete_url = reverse('labels:delete', kwargs={'pk': 3})
        redir_url = build_login_url(delete_url)

        response = self.client.post(delete_url, follow=True)

        self.assertRedirects(response, redir_url)
        self.assertContains(response, 'alert-danger')

    def test_label_delete_with_tasks(self):
        login_test_user(self.client)

        # Label 1 has associated tasks, should not delete
        delete_url = reverse('labels:delete', kwargs={'pk': 1})
        redir_url = reverse('labels:index')

        response = self.client.post(delete_url, follow=True)

        self.assertRedirects(response, redir_url)
        self.assertContains(response, 'alert-danger')

        # Check that entry was not deleted
        db_entry = Label.objects.get(pk=1)
        self.assertIsNotNone(db_entry)
