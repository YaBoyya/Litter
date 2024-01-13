from django.test import TestCase
from django.urls import reverse

from .models import LitterUser


class UserLoginTest(TestCase):
    def setUp(self):
        self.test_view = reverse('users:login')
        self.credentials = {'usertag': 'test',
                            'email': 'test@example.com',
                            'password': 'TestTest123'}
        self.test_user = LitterUser.objects.create_user(**self.credentials)

    def test_user_login_loads(self):
        response = self.client.get(self.test_view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login-register.html')

    def test_user_login_post_blank_data(self):
        response = self.client.post(self.test_view, {})
        self.assertFormError(response, 'form',
                             'usertag', 'This field is required.')
        self.assertFormError(response, 'form',
                             'password', 'This field is required.')

    def test_user_login_is_none(self):
        response = self.client.post(self.test_view,
                                    {'usertag': 'wrong',
                                     'password': 'Credentials'})
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid usertag or password.")

    def test_user_login_success(self):
        response = self.client.post(self.test_view,
                                    self.credentials,
                                    follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('core:feed'))
