from django.test import TestCase

# Create your tests here.
class SimpleTest(TestCase):
    def test_register(self):
        response = self.client.post('/register/', {'username': 'test', 'password': 'test'}, follow=True)
        self.assertRedirects(response, '/login/')

    def test_login(self):
        response = self.client.post('/register/', {'username': 'test', 'password': 'test'}, follow=True)

        response = self.client.post('/login/', {'username': 'test', 'password': 'test'}, follow=True)
        self.assertRedirects(response, '/')