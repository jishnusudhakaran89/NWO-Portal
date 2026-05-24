from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from inventory.defaults import DEFAULT_PASSWORDS


class AuthenticationBackendTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='nwo_kochi',
            email='nwo_kochi@nwo.in',
            password='Nwo@Kochi@2026!'
        )

    def test_case_insensitive_username_login(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'NWO_KOCHI', 'password': 'Nwo@Kochi@2026!'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_email_login(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'nwo_kochi@nwo.in', 'password': 'Nwo@Kochi@2026!'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_default_password_mapping(self):
        self.assertEqual(DEFAULT_PASSWORDS['NWO KOCHI'], 'Nwo@Kochi@2026!')
        self.assertEqual(DEFAULT_PASSWORDS['NWO TRIPUNITHARA'], 'Nwo@Tripunithara@2026!')
