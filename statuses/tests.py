from django.test import TestCase
from django.urls import reverse

from .models import Status


class StatusesTestCase(TestCase):
    fixtures = ['statuses.json', 'users.json']

    def test_statuses_read(self):
        login_user = {
            'username': 'test_user',
            'password': 'password'
        }
        self.client.login(**login_user)

        response = self.client.get(reverse('statuses:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New')
        self.assertContains(response, 'In progress')
        self.assertContains(response, 'Closed')

    def test_statuses_read_anonymous(self):
        req_path = reverse('statuses:index')
        redirect_path = f'{reverse("users:login")}?next={req_path}'
        response = self.client.get(req_path, follow=True)
        self.assertRedirects(response, redirect_path)
        self.assertContains(response, 'alert-danger')

    def test_statuses_create(self):
        login_user = {
            'username': 'test_user',
            'password': 'password'
        }
        self.client.login(**login_user)

        status = {
            'name': 'Test'
        }

        response = self.client.post(
            reverse('statuses:create'),
            data=status
        )
        self.assertRedirects(response, reverse('statuses:index'))

    def test_statuses_create_anonymous(self):
        req_path = reverse('statuses:create')
        redirect_path = f'{reverse("users:login")}?next={req_path}'
        status = {
            'name': 'Test'
        }
        response = self.client.post(req_path, data=status, follow=True)
        self.assertRedirects(response, redirect_path)
        self.assertContains(response, 'alert-danger')

    def test_statuses_update(self):
        login_user = {
            'username': 'test_user',
            'password': 'password'
        }
        self.client.login(**login_user)

        status = {
            'name': 'Test'
        }

        response = self.client.post(
            reverse('statuses:update', kwargs={'pk': 1}),
            data=status
        )
        self.assertRedirects(response, reverse('statuses:index'))

        db_status = Status.objects.get(pk=1)
        self.assertEqual(db_status.name, 'Test')

    def test_statuses_update_anonymous(self):
        req_path = reverse('statuses:update', kwargs={'pk': 1})
        redirect_path = f'{reverse("users:login")}?next={req_path}'
        status = {
            'name': 'Test'
        }
        response = self.client.post(req_path, data=status, follow=True)
        self.assertRedirects(response, redirect_path)
        self.assertContains(response, 'alert-danger')

    def test_statuses_delete(self):
        login_user = {
            'username': 'test_user',
            'password': 'password'
        }
        self.client.login(**login_user)

        response = self.client.post(
            reverse('statuses:delete', kwargs={'pk': 1})
        )
        self.assertRedirects(response, reverse('statuses:index'))

        with self.assertRaisesMessage(Status.DoesNotExist, ''):
            Status.objects.get(pk=1)

    def test_statuses_delete_anonymous(self):
        req_path = reverse('statuses:delete', kwargs={'pk': 1})
        redirect_path = f'{reverse("users:login")}?next={req_path}'
        response = self.client.post(req_path, follow=True)
        self.assertRedirects(response, redirect_path)
        self.assertContains(response, 'alert-danger')
