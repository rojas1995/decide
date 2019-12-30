
# Create your tests here.
class SimpleTest(TestCase):
def test_register(Self):

    response = self.client.post('/register', { 'username': 'pedro', 'password': 'pedropedro'})
    self.assertRedirects(response, '/login')