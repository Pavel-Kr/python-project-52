from django.test import Client, TestCase
from django.urls import reverse_lazy as rl, reverse
from django.contrib.auth.models import User


def login_test_user(client: Client, credentials=None):
    if not credentials:
        credentials = {
            'username': 'test_user',
            'password': 'password'
        }
    client.login(**credentials)


class UsersTestCase(TestCase):
    fixtures = [
        'users.json',
        'tasks.json',
        'statuses.json'
    ]

    def test_create_user(self):
        test_user = {
            'username': 'test_user3',
            'password1': 'gfccdjhl1',
            'password2': 'gfccdjhl1'
        }
        response = self.client.post(rl('users:create'),
                                    data=test_user,
                                    follow=False)
        self.assertRedirects(response, rl('login'))
        db_user = User.objects.get(username='test_user')
        self.assertIsNotNone(db_user)

    def test_update_user(self):
        # Authenticate as test user
        login_test_user(self.client)
        # Update user
        user = User.objects.get(username='test_user')
        update_path = reverse('users:update', kwargs={'pk': user.pk})
        update_data = {
            'first_name': 'Testname',
            # Save the password
            'username': 'test_user',
            'password1': 'gfccdjhl1',
            'password2': 'gfccdjhl1'
        }
        response = self.client.post(update_path, update_data)
        # Check that request succeded
        self.assertRedirects(response, reverse('users:index'))
        # Check that user is updated in the database
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Testname')

    def test_update_user_from_anonymous(self):
        update_path = reverse('users:update', kwargs={'pk': 1})
        redirect_path = f"{reverse('login')}?next={update_path}"
        response = self.client.post(update_path)
        self.assertRedirects(response, redirect_path)

    def test_update_user_from_another_user(self):
        login_test_user(self.client)
        # Try to update test user 2
        user_2 = User.objects.get(username='test_user2')
        update_path = reverse('users:update', kwargs={'pk': user_2.pk})
        redirect_path = reverse('users:index')
        response = self.client.post(update_path, follow=True)
        self.assertRedirects(response, redirect_path)
        # Check that we display error message
        self.assertContains(response, 'alert-danger')

    def test_delete_user(self):
        # Login as test_user2 as he doesn't have any tasks assigned to him
        credentials = {
            'username': 'test_user2',
            'password': 'gfccdjhl1'
        }
        login_test_user(self.client, credentials)
        # Try to delete user
        user = User.objects.get(username='test_user2')
        delete_path = reverse('users:delete', kwargs={'pk': user.pk})
        response = self.client.post(delete_path)
        redirect_path = reverse('users:index')
        self.assertRedirects(response, redirect_path)
        # Check that user has been deleted
        with self.assertRaisesMessage(User.DoesNotExist,
                                      'does not exist'):
            User.objects.get(username='test_user2')

    def test_delete_user_from_anonymous(self):
        delete_path = reverse('users:delete', kwargs={'pk': 1})
        redirect_path = f"{reverse('login')}?next={delete_path}"
        response = self.client.get(delete_path)
        self.assertRedirects(response, redirect_path)

    def test_delete_user_from_another_user(self):
        login_test_user(self.client)
        # Try to delete test user 2
        user_2 = User.objects.get(username='test_user2')
        update_path = reverse('users:delete', kwargs={'pk': user_2.pk})
        redirect_path = reverse('users:index')
        response = self.client.post(update_path, follow=True)
        self.assertRedirects(response, redirect_path)
        # Check that we display error message
        self.assertContains(response, 'alert-danger')

    def test_delete_user_with_tasks(self):
        # test_user has tasks, should not be deleted
        login_test_user(self.client)
        # Try to delete test_user
        user = User.objects.get(username='test_user')
        delete_path = reverse('users:delete', kwargs={'pk': user.pk})
        redirect_path = reverse('users:index')
        response = self.client.post(delete_path, follow=True)
        self.assertRedirects(response, redirect_path)
        # Check that we display error message
        self.assertContains(response, 'alert-danger')
        # Check that user has not been deleted
        db_entry = User.objects.get(username='test_user')
        self.assertIsNotNone(db_entry)
