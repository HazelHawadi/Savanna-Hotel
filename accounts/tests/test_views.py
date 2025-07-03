from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialApp


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_view_post_valid(self):
        data = {
            'username': 'testuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        }
        response = self.client.post(self.register_url, data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(response.context['user'].is_authenticated)

    def test_register_view_post_invalid(self):
        data = {
            'username': 'baduser',
            'password1': 'pass',
            'password2': 'word',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='baduser').exists())
        self.assertFalse(response.context['user'].is_authenticated)


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.password = 'PasswordTest123!'
        self.user = User.objects.create_user(username='testuser', password=self.password)

        self.social_app = SocialApp.objects.create(
            provider='facebook',
            name='Facebook',
            client_id='fake',
            secret='fake',
        )
        self.social_app.sites.add(4)

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_view_post_valid(self):
        response = self.client.post(self.login_url, {
            'username': self.user.username,
            'password': self.password
        }, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_view_post_invalid(self):
        response = self.client.post(self.login_url, {
            'username': self.user.username,
            'password': 'wrongpass'
        })
        self.assertFalse(response.context['user'].is_authenticated)

    def test_remember_me_sets_long_expiry(self):
        response = self.client.post(self.login_url, {
            'username': self.user.username,
            'password': self.password,
            'remember_me': 'on'
        }, follow=True)
        self.assertGreaterEqual(self.client.session.get_expiry_age(), 31536000 - 60)

    def test_no_remember_me_sets_session_to_close(self):
        response = self.client.post(self.login_url, {
            'username': self.user.username,
            'password': self.password,
        }, follow=True)
        self.assertTrue(self.client.session.get_expire_at_browser_close())


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('accounts:logout')
        self.user = User.objects.create_user(username='testuser', password='Testpass123!')
        self.client.login(username='testuser', password='Testpass123!')

    def test_logout_view(self):
        response = self.client.get(self.logout_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
