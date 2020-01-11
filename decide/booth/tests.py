from django.test import TestCase

# Create your tests here.
class SimpleTest(TestCase):
    def test_register(self):
        response = self.client.post('/register/', {
            'username': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@test.com',
            'password': 'test',
            'confirm_password': 'test'
        }, follow=True)
        self.assertRedirects(response, '/login/')

    def test_register2(self):
        response = self.client.post('/register/', {
            'username': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@test.com',
            'password': 'test',
            'confirm_password': 'test'
        }, follow=True)

        response = self.client.post('/register/', {
            'username': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@test.com',
            'password': 'test',
            'confirm_password': 'test'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post('/register/', {
            'username': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@test.com',
            'password': 'test',
            'confirm_password': 'test'
        }, follow=True)

        response = self.client.post('/login/', {'username': 'test', 'password': 'test'}, follow=True)
        self.assertRedirects(response, '/')

    def test_login2(self):
        response = self.client.post('/login/', {'username': 'test22', 'password': 'test22'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        response = self.client.post('/register/', {
            'username': 'test3',
            'first_name': 'test3',
            'last_name': 'test3',
            'email': 'test3@test.com',
            'password': 'test3',
            'confirm_password': 'test3'
        }, follow=True)

        response = self.client.post('/login/', {'username': 'test3', 'password': 'test3'}, follow=True)

        response = self.client.post('/profile/', {
            'first_name': 'test2',
            'last_name': 'test2',
            'email': 'test2@test.com',
        }, follow=True)

        self.assertEqual(response.status_code, 200)