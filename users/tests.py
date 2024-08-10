from django.test import TestCase
from django.urls import reverse_lazy as rl, reverse
from django.contrib.auth.models import User


class UsersTestCase(TestCase):
    fixtures = ['data.json']

    def test_create_user(self):
        test_user = {
            'username': 'test_user',
            'password1': 'gfccdjhl1',
            'password2': 'gfccdjhl1'
        }
        response = self.client.post(rl('users:create'),
                                    data=test_user,
                                    follow=False)
        self.assertRedirects(response, rl('users:login'))
        db_user = User.objects.get(username='test_user')
        self.assertIsNotNone(db_user)

    def test_update_user(self):
        login_user = {
            'username': 'test_user1',
            'password': 'gfccdjhl1'
        }
        # Authenticate as test user 1
        login_path = reverse('users:login')
        self.client.post(login_path, login_user)
        # Update user
        user_1 = User.objects.get(username='test_user1')
        update_path = reverse('users:update', kwargs={'pk': user_1.pk})
        update_data = {
            'first_name': 'Testname',
            # Save the password
            'username': 'test_user1',
            'password1': 'gfccdjhl1',
            'password2': 'gfccdjhl1'
        }
        response = self.client.post(update_path, update_data)
        # Check that request succeded
        self.assertRedirects(response, reverse('users:index'))
        # Check that user is updated in the database
        user_1.refresh_from_db()
        self.assertEqual(user_1.first_name, 'Testname')

    def test_update_user_from_anonymous(self):
        update_path = reverse('users:update', kwargs={'pk': 1})
        redirect_path = f"{reverse('users:login')}?next={update_path}"
        response = self.client.post(update_path)
        self.assertRedirects(response, redirect_path)

    def test_update_user_from_another_user(self):
        login_user = {
            'username': 'test_user1',
            'password': 'gfccdjhl1'
        }
        # Authenticate as test user 1
        login_path = reverse('users:login')
        self.client.post(login_path, login_user)
        # Try to update test user 2
        user_2 = User.objects.get(username='test_user2')
        update_path = reverse('users:update', kwargs={'pk': user_2.pk})
        redirect_path = reverse('users:index')
        response = self.client.post(update_path, follow=True)
        self.assertRedirects(response, redirect_path)
        # Check that we display error message
        self.assertContains(response, 'alert-danger')

    def test_delete_user(self):
        login_user = {
            'username': 'test_user1',
            'password': 'gfccdjhl1'
        }
        # Authenticate as test user 1
        login_path = reverse('users:login')
        self.client.post(login_path, login_user)
        # Try to delete user
        user_1 = User.objects.get(username='test_user1')
        delete_path = reverse('users:delete', kwargs={'pk': user_1.pk})
        response = self.client.post(delete_path)
        redirect_path = reverse('users:index')
        self.assertRedirects(response, redirect_path)
        # Check that user has been deleted
        with self.assertRaisesMessage(User.DoesNotExist,
                                      'does not exist'):
            User.objects.get(username='test_user1')

    def test_delete_user_from_anonymous(self):
        delete_path = reverse('users:delete', kwargs={'pk': 1})
        redirect_path = f"{reverse('users:login')}?next={delete_path}"
        response = self.client.get(delete_path)
        self.assertRedirects(response, redirect_path)

    def test_delete_user_from_another_user(self):
        login_user = {
            'username': 'test_user1',
            'password': 'gfccdjhl1'
        }
        # Authenticate as test user 1
        login_path = reverse('users:login')
        self.client.post(login_path, login_user)
        # Try to update test user 2
        user_2 = User.objects.get(username='test_user2')
        update_path = reverse('users:delete', kwargs={'pk': user_2.pk})
        redirect_path = reverse('users:index')
        response = self.client.post(update_path, follow=True)
        self.assertRedirects(response, redirect_path)
        # Check that we display error message
        self.assertContains(response, 'alert-danger')
