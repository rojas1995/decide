from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None
    
    def test_identity(self):
        data = {
            'type': 'IDENTITY',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_simple(self):
        data = {
            'type': 'SIMPLE',
            'seats':7,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 }, #2.285
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
        
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 2 },#0.188
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 2 },#0.188
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 1 },#0.31
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 1 },#0.14
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },#0.285
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_simple1(self):
        data = {
            'type': 'SIMPLE',
            'seats':40,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 13 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 13 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 7 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 5 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 2 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)



    def test_simple2(self):
        data = {
            'type': 'SIMPLE',
            'seats': 50,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 10 },
                { 'option': 'Option 2', 'number': 2, 'votes': 20 },
                { 'option': 'Option 3', 'number': 3, 'votes': 45 },
                { 'option': 'Option 4', 'number': 4, 'votes': 15 },
                { 'option': 'Option 5', 'number': 5, 'votes': 8  },
                { 'option': 'Option 6', 'number': 6, 'votes': 2 },
            ]
        }

        expected_result = [
            { 'option': 'Option 3', 'number': 3, 'votes': 45, 'postproc': 23 },
            { 'option': 'Option 2', 'number': 2, 'votes': 20, 'postproc': 10 },
            { 'option': 'Option 4', 'number': 4, 'votes': 15, 'postproc': 7 },
            { 'option': 'Option 1', 'number': 1, 'votes': 10, 'postproc': 5 },
            { 'option': 'Option 5', 'number': 5, 'votes': 8, 'postproc': 4 },
            { 'option': 'Option 6', 'number': 6, 'votes': 2, 'postproc': 1 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_simple3(self):
        data = {
            'type': 'SIMPLE',
            'seats': 100,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 200 },
                { 'option': 'Option 2', 'number': 2, 'votes': 50 },
                { 'option': 'Option 3', 'number': 3, 'votes': 500 },
                { 'option': 'Option 4', 'number': 4, 'votes': 100 },
                { 'option': 'Option 5', 'number': 5, 'votes': 60 },
                { 'option': 'Option 6', 'number': 6, 'votes': 90 },
            ]
        }

        expected_result = [
            { 'option': 'Option 3', 'number': 3, 'votes': 500, 'postproc': 50 },
            { 'option': 'Option 1', 'number': 1, 'votes': 200, 'postproc': 20 },
            { 'option': 'Option 4', 'number': 4, 'votes': 100, 'postproc': 10 },
            { 'option': 'Option 6', 'number': 6, 'votes': 90, 'postproc': 9 },
            { 'option': 'Option 5', 'number': 5, 'votes': 60, 'postproc': 6 },
            { 'option': 'Option 2', 'number': 2, 'votes': 50, 'postproc': 5 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_simple4(self):
        data = {
            'type': 'SIMPLE',
            'seats': 200,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5000 },
                { 'option': 'Option 2', 'number': 2, 'votes': 2000 },
                { 'option': 'Option 3', 'number': 3, 'votes': 1000 },
                { 'option': 'Option 4', 'number': 4, 'votes': 500 },
                { 'option': 'Option 5', 'number': 5, 'votes': 800 },
                { 'option': 'Option 6', 'number': 6, 'votes': 700 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5000, 'postproc': 100 },
            { 'option': 'Option 2', 'number': 2, 'votes': 2000, 'postproc': 40 },
            { 'option': 'Option 3', 'number': 3, 'votes': 1000, 'postproc': 20 },
            { 'option': 'Option 5', 'number': 5, 'votes': 800, 'postproc': 16 },
            { 'option': 'Option 6', 'number': 6, 'votes': 700, 'postproc': 14 },
            { 'option': 'Option 4', 'number': 4, 'votes': 500, 'postproc': 10 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

   
    def test_simple5(self):
        data = {
            'type': 'SIMPLE',
            'seats': 250,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 10000 },#20000/250=80
                { 'option': 'Option 2', 'number': 2, 'votes': 6000 },
                { 'option': 'Option 3', 'number': 3, 'votes': 1000 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2000 },
                { 'option': 'Option 5', 'number': 5, 'votes': 500 },
                { 'option': 'Option 6', 'number': 6, 'votes': 500 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 10000, 'postproc': 125 },
            { 'option': 'Option 2', 'number': 2, 'votes': 6000, 'postproc': 75 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2000, 'postproc': 25 },
            { 'option': 'Option 3', 'number': 3, 'votes': 1000, 'postproc': 13 },
            { 'option': 'Option 5', 'number': 5, 'votes': 500, 'postproc': 6 },
            { 'option': 'Option 6', 'number': 6, 'votes': 500, 'postproc': 6 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_simple6(self):
        data = {
            'type': 'SIMPLE',
            'seats': 20,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 10 }, #105/20 = 5.25
                { 'option': 'Option 2', 'number': 2, 'votes': 20 },
                { 'option': 'Option 3', 'number': 3, 'votes': 60 },
                { 'option': 'Option 4', 'number': 4, 'votes': 10 },
                { 'option': 'Option 5', 'number': 5, 'votes': 3 },
                { 'option': 'Option 6', 'number': 6, 'votes': 2 },
            ]
        }

        expected_result = [
            { 'option': 'Option 3', 'number': 3, 'votes': 60, 'postproc': 11 }, #0.42
            { 'option': 'Option 2', 'number': 2, 'votes': 20, 'postproc': 4 },#0.809
            { 'option': 'Option 1', 'number': 1, 'votes': 10, 'postproc': 2 },#0.904
            { 'option': 'Option 4', 'number': 4, 'votes': 10, 'postproc': 2 },#0.904
            { 'option': 'Option 5', 'number': 5, 'votes': 3, 'postproc': 1 },
            { 'option': 'Option 6', 'number': 6, 'votes': 2, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
        
    def test_simple7(self):
        data = {
            'type': 'SIMPLE',
            'seats': 100,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 100 }, #3
                { 'option': 'Option 2', 'number': 2, 'votes': 50 },
                { 'option': 'Option 3', 'number': 3, 'votes': 9 },
                { 'option': 'Option 4', 'number': 4, 'votes':  20},
                { 'option': 'Option 5', 'number': 5, 'votes': 40 },
                { 'option': 'Option 6', 'number': 6, 'votes': 81 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 100, 'postproc': 33 },#0.333
            { 'option': 'Option 6', 'number': 6, 'votes': 81, 'postproc': 27 },
            { 'option': 'Option 2', 'number': 2, 'votes': 50, 'postproc': 17 },#0.666
            { 'option': 'Option 5', 'number': 5, 'votes': 40, 'postproc': 13 },#0.333
            { 'option': 'Option 4', 'number': 4, 'votes': 20, 'postproc': 7 },#0.666
            { 'option': 'Option 3', 'number': 3, 'votes': 9, 'postproc': 3 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_simple8(self):
        data = {
            'type': 'SIMPLE',
            'seats': 500,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 10000 },
                { 'option': 'Option 2', 'number': 2, 'votes': 20000 },
                { 'option': 'Option 3', 'number': 3, 'votes': 500 },
                { 'option': 'Option 4', 'number': 4, 'votes':  400},
                { 'option': 'Option 5', 'number': 5, 'votes': 15000 },
                { 'option': 'Option 6', 'number': 6, 'votes': 4100 },
            ]
        }

        expected_result = [
            { 'option': 'Option 2', 'number': 2, 'votes': 20000, 'postproc': 200 },
            { 'option': 'Option 5', 'number': 5, 'votes': 15000, 'postproc': 150 },
            { 'option': 'Option 1', 'number': 1, 'votes': 10000, 'postproc':  100},
            { 'option': 'Option 6', 'number': 6, 'votes': 4100, 'postproc': 41 },
            { 'option': 'Option 3', 'number': 3, 'votes': 500, 'postproc': 5 },
            { 'option': 'Option 4', 'number': 4, 'votes': 400, 'postproc': 4 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
