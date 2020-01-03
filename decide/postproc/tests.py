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
            'seats':7
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
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 2 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 2 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 1 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 1 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_simple1(self):
        data = {
            'type': 'SIMPLE',
            'seats':40
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
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 2 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 2 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 1 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 1 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

          //Codigo Pablo Reneses

      def test_simple2(self):
        data = {
            'type': 'SIMPLE',
            'seats': 50,
            'options': [
                { 'option': 'Partido 1', 'number': 1, 'votes': 10 },
                { 'option': 'Partido 2', 'number': 2, 'votes': 20 },
                { 'option': 'Partido 3', 'number': 3, 'votes': 45 },
                { 'option': 'Partido 4', 'number': 4, 'votes': 15 },
                { 'option': 'Partido 5', 'number': 5, 'votes': 8  },
                { 'option': 'Partido 6', 'number': 6, 'votes': 2 },
            ]
        }

        expected_result = [
            { 'option': 'Partido 6', 'number': 3, 'votes': 45, 'postproc': 23 },
            { 'option': 'Partido 5', 'number': 2, 'votes': 20, 'postproc': 10 },
            { 'option': 'Partido 1', 'number': 4, 'votes': 15, 'postproc': 7 },
            { 'option': 'Partido 3', 'number': 1, 'votes': 10, 'postproc': 5 },
            { 'option': 'Partido 4', 'number': 5, 'votes': 8, 'postproc': 4 },
            { 'option': 'Partido 2', 'number': 6, 'votes': 2, 'postproc': 1 },
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
                { 'option': 'Partido 1', 'number': 1, 'votes': 200 },
                { 'option': 'Partido 2', 'number': 2, 'votes': 50 },
                { 'option': 'Partido 3', 'number': 3, 'votes': 500 },
                { 'option': 'Partido 4', 'number': 4, 'votes': 100 },
                { 'option': 'Partido 5', 'number': 5, 'votes': 60 },
                { 'option': 'Partido 6', 'number': 6, 'votes': 90 },
            ]
        }

        expected_result = [
            { 'option': 'Partido 6', 'number': 3, 'votes': 500, 'postproc': 50 },
            { 'option': 'Partido 5', 'number': 1, 'votes': 200, 'postproc': 20 },
            { 'option': 'Partido 1', 'number': 4, 'votes': 100, 'postproc': 10 },
            { 'option': 'Partido 3', 'number': 6, 'votes': 90, 'postproc': 9 },
            { 'option': 'Partido 4', 'number': 5, 'votes': 60, 'postproc': 6 },
            { 'option': 'Partido 2', 'number': 2, 'votes': 50, 'postproc': 5 },
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
                { 'option': 'Partido 1', 'number': 1, 'votes': 5000 },
                { 'option': 'Partido 2', 'number': 2, 'votes': 2000 },
                { 'option': 'Partido 3', 'number': 3, 'votes': 1000 },
                { 'option': 'Partido 4', 'number': 4, 'votes': 500 },
                { 'option': 'Partido 5', 'number': 5, 'votes': 800 },
                { 'option': 'Partido 6', 'number': 6, 'votes': 700 },
            ]
        }

        expected_result = [
            { 'option': 'Partido 2', 'number': 1, 'votes': 5000, 'postproc': 100 },
            { 'option': 'Partido 1', 'number': 2, 'votes': 2000, 'postproc': 40 },
            { 'option': 'Partido 3', 'number': 3, 'votes': 1000, 'postproc': 20 },
            { 'option': 'Partido 4', 'number': 5, 'votes': 800, 'postproc': 16 },
            { 'option': 'Partido 6', 'number': 6, 'votes': 700, 'postproc': 14 },
            { 'option': 'Partido 5', 'number': 4, 'votes': 500, 'postproc': 10 },
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
                { 'option': 'Partido 1', 'number': 1, 'votes': 10000 },
                { 'option': 'Partido 2', 'number': 2, 'votes': 6000 },
                { 'option': 'Partido 3', 'number': 3, 'votes': 1000 },
                { 'option': 'Partido 4', 'number': 4, 'votes': 2000 },
                { 'option': 'Partido 5', 'number': 5, 'votes': 500 },
                { 'option': 'Partido 6', 'number': 6, 'votes': 500 },
            ]
        }

        expected_result = [
            { 'option': 'Partido 1', 'number': 1, 'votes': 10000, 'postproc': 125 },
            { 'option': 'Partido 2', 'number': 2, 'votes': 6000, 'postproc': 75 },
            { 'option': 'Partido 4', 'number': 4, 'votes': 2000, 'postproc': 25 },
            { 'option': 'Partido 3', 'number': 3, 'votes': 1000, 'postproc': 13 },
            { 'option': 'Partido 5', 'number': 5, 'votes': 500, 'postproc': 6 },
            { 'option': 'Partido 6', 'number': 6, 'votes': 500, 'postproc': 6 },
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
                { 'option': 'Partido 1', 'number': 1, 'votes': 10 },
                { 'option': 'Partido 2', 'number': 2, 'votes': 20 },
                { 'option': 'Partido 3', 'number': 3, 'votes': 60 },
                { 'option': 'Partido 4', 'number': 4, 'votes': 10 },
                { 'option': 'Partido 5', 'number': 5, 'votes': 3 },
                { 'option': 'Partido 6', 'number': 6, 'votes': 2 },
            ]
        }

        expected_result = [
            { 'option': 'Partido 1', 'number': 3, 'votes': 60, 'postproc': 12 },
            { 'option': 'Partido 4', 'number': 2, 'votes': 20, 'postproc': 4 },
            { 'option': 'Partido 3', 'number': 4, 'votes': 10, 'postproc': 2 },
            { 'option': 'Partido 6', 'number': 1, 'votes': 10, 'postproc': 2 },
            { 'option': 'Partido 5', 'number': 5, 'votes': 3, 'postproc': 0 },
            { 'option': 'Partido 2', 'number': 6, 'votes': 2, 'postproc': 0 },
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
                { 'option': 'Partido 1', 'number': 1, 'votes': 100 },
                { 'option': 'Partido 2', 'number': 2, 'votes': 50 },
                { 'option': 'Partido 3', 'number': 3, 'votes': 9 },
                { 'option': 'Partido 4', 'number': 4, 'votes':  20},
                { 'option': 'Partido 5', 'number': 5, 'votes': 40 },
                { 'option': 'Partido 6', 'number': 6, 'votes': 81 },
            ]
        }

        expected_result = [
            { 'option': 'Partido 1', 'number': 1, 'votes': 100, 'postproc': 33 },
            { 'option': 'Partido 6', 'number': 6, 'votes': 81, 'postproc': 27 },
            { 'option': 'Partido 2', 'number': 2, 'votes': 50, 'postproc': 16 },
            { 'option': 'Partido 5', 'number': 5, 'votes': 40, 'postproc': 13 },
            { 'option': 'Partido 4', 'number': 4, 'votes': 20, 'postproc': 6 },
            { 'option': 'Partido 3', 'number': 3, 'votes': 9, 'postproc': 3 },
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
                { 'option': 'Partido 1', 'number': 1, 'votes': 10000 },
                { 'option': 'Partido 2', 'number': 2, 'votes': 20000 },
                { 'option': 'Partido 3', 'number': 3, 'votes': 500 },
                { 'option': 'Partido 4', 'number': 4, 'votes':  400},
                { 'option': 'Partido 5', 'number': 5, 'votes': 15000 },
                { 'option': 'Partido 6', 'number': 6, 'votes': 4100 },
            ]
        }

        expected_result = [
            { 'option': 'Partido 2', 'number': 2, 'votes': 20000, 'postproc': 200 },
            { 'option': 'Partido 6', 'number': 6, 'votes': 15000, 'postproc': 150 },
            { 'option': 'Partido 2', 'number': 2, 'votes': 10000, 'postproc':  100},
            { 'option': 'Partido 5', 'number': 5, 'votes': 4100, 'postproc': 41 },
            { 'option': 'Partido 4', 'number': 4, 'votes': 500, 'postproc': 5 },
            { 'option': 'Partido 3', 'number': 3, 'votes': 400, 'postproc': 4 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

        def test_simple9(self):
        data = {
            'type': 'SIMPLE',
            'seats': 2000,
            'options': [
                { 'option': 'Partido 1', 'number': 1, 'votes': 10000 },
                { 'option': 'Partido 2', 'number': 2, 'votes': 20000 },
                { 'option': 'Partido 3', 'number': 3, 'votes': 500 },
                { 'option': 'Partido 4', 'number': 4, 'votes':  400},
                { 'option': 'Partido 5', 'number': 5, 'votes': 15000 },
                { 'option': 'Partido 6', 'number': 6, 'votes': 4100 },
                { 'option': 'Partido 7', 'number': 7, 'votes': 4100 },
                { 'option': 'Partido 8', 'number': 8, 'votes': 4100 },
                { 'option': 'Partido 9', 'number': 9, 'votes': 4100 },
                { 'option': 'Partido 10', 'number': 10, 'votes': 4100 },

            ]
        }

        expected_result = [
            { 'option': 'Partido 2', 'number': 2, 'votes': 20000, 'postproc': 200 },
            { 'option': 'Partido 6', 'number': 6, 'votes': 15000, 'postproc': 150 },
            { 'option': 'Partido 2', 'number': 2, 'votes': 10000, 'postproc':  100},
            { 'option': 'Partido 5', 'number': 5, 'votes': 4100, 'postproc': 41 },
            { 'option': 'Partido 4', 'number': 4, 'votes': 500, 'postproc': 5 },
            { 'option': 'Partido 3', 'number': 3, 'votes': 400, 'postproc': 4 },
            { 'option': 'Partido 3', 'number': 3, 'votes': 400, 'postproc': 4 },
            { 'option': 'Partido 3', 'number': 3, 'votes': 400, 'postproc': 4 },
            { 'option': 'Partido 3', 'number': 3, 'votes': 400, 'postproc': 4 },
            { 'option': 'Partido 3', 'number': 3, 'votes': 400, 'postproc': 4 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)