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

    def test_dhondt1(self):
        data = {
            'type': 'DHONDT',
            'seats': 12,
            'options': [
                { 'option': 'Partido 1', 'number': 1, 'votes': 50 },
                { 'option': 'Partido 2', 'number': 2, 'votes': 10 },
                { 'option': 'Partido 3', 'number': 3, 'votes': 34 },
                { 'option': 'Partido 4', 'number': 4, 'votes': 25 },
                { 'option': 'Partido 5', 'number': 5, 'votes': 56 },
                { 'option': 'Partido 6', 'number': 6, 'votes': 170 },
            ]
        }

        expected_result = [
            { 'option': 'Partido 6', 'number': 6, 'votes': 170, 'postproc': 6 },
            { 'option': 'Partido 5', 'number': 5, 'votes': 56, 'postproc': 2 },
            { 'option': 'Partido 1', 'number': 1, 'votes': 50, 'postproc': 2 },
            { 'option': 'Partido 3', 'number': 3, 'votes': 34, 'postproc': 1 },
            { 'option': 'Partido 4', 'number': 4, 'votes': 25, 'postproc': 1 },
            { 'option': 'Partido 2', 'number': 2, 'votes': 10, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_dhondt2(self):
        data = {
            'type': 'DHONDT',
            'seats': 17,
            'options': [
                { 'option': 'Partido 1', 'number': 1, 'votes': 50 },
                { 'option': 'Partido 2', 'number': 2, 'votes': 10 },
                { 'option': 'Partido 3', 'number': 3, 'votes': 34 },
                { 'option': 'Partido 4', 'number': 4, 'votes': 25 },
                { 'option': 'Partido 5', 'number': 5, 'votes': 56 },
                { 'option': 'Partido 6', 'number': 6, 'votes': 1000000 },
            ]
        }

        expected_result = [
            { 'option': 'Partido 6', 'number': 6, 'votes': 1000000, 'postproc': 17 },
            { 'option': 'Partido 5', 'number': 5, 'votes': 56, 'postproc': 0 },
            { 'option': 'Partido 1', 'number': 1, 'votes': 50, 'postproc': 0 },
            { 'option': 'Partido 3', 'number': 3, 'votes': 34, 'postproc': 0 },
            { 'option': 'Partido 4', 'number': 4, 'votes': 25, 'postproc': 0 },
            { 'option': 'Partido 2', 'number': 2, 'votes': 10, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_dhondt3(self):
        data = {
            'type': 'DHONDT',
            'seats': 2,
            'options': [
                { 'option': 'Partido 1', 'number': 1, 'votes': 2000 },
                { 'option': 'Partido 2', 'number': 2, 'votes': 4000 },
                { 'option': 'Partido 3', 'number': 3, 'votes': 1999 },
                { 'option': 'Partido 4', 'number': 4, 'votes': 1998 },
                { 'option': 'Partido 5', 'number': 5, 'votes': 56 },
                { 'option': 'Partido 6', 'number': 6, 'votes': 170 },
            ]
        }

        expected_result = [
            { 'option': 'Partido 2', 'number': 2, 'votes': 4000, 'postproc': 2 },
            { 'option': 'Partido 1', 'number': 1, 'votes': 2000, 'postproc': 0 },
            { 'option': 'Partido 3', 'number': 3, 'votes': 1999, 'postproc': 0 },
            { 'option': 'Partido 4', 'number': 4, 'votes': 1998, 'postproc': 0 },
            { 'option': 'Partido 6', 'number': 6, 'votes': 170, 'postproc': 0 },
            { 'option': 'Partido 5', 'number': 5, 'votes': 56, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

def test_dhondt4(self):
        data = {
            'type': 'DHONDT',
            'seats': 12,
            'options': [
                { 'option': 'Partido 1', 'number': 1, 'votes': 10000 },
                { 'option': 'Partido 2', 'number': 2, 'votes': 6000 },
                { 'option': 'Partido 3', 'number': 3, 'votes': 1000 },
                { 'option': 'Partido 4', 'number': 4, 'votes': 3000 },
                { 'option': 'Partido 5', 'number': 5, 'votes': 500 },
                { 'option': 'Partido 6', 'number': 6, 'votes': 500 },
            ]
        }

        expected_result = [
            { 'option': 'Partido 1', 'number': 1, 'votes': 10000, 'postproc': 6 },
            { 'option': 'Partido 2', 'number': 2, 'votes': 6000, 'postproc': 4 },
            { 'option': 'Partido 4', 'number': 4, 'votes': 3000, 'postproc': 2 },
            { 'option': 'Partido 3', 'number': 3, 'votes': 1000, 'postproc': 0 },
            { 'option': 'Partido 5', 'number': 5, 'votes': 500, 'postproc': 0 },
            { 'option': 'Partido 6', 'number': 6, 'votes': 500, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

def test_dhondt5(self):
        data = {
            'type': 'DHONDT',
            'seats': 21,
            'options': [
                { 'option': 'Partido 1', 'number': 1, 'votes': 24000 },
                { 'option': 'Partido 2', 'number': 2, 'votes': 4000 },
                { 'option': 'Partido 3', 'number': 3, 'votes': 8000 },
                { 'option': 'Partido 4', 'number': 4, 'votes': 12000 },
                { 'option': 'Partido 5', 'number': 5, 'votes': 4800 },
                { 'option': 'Partido 6', 'number': 6, 'votes': 6000 },
            ]
        }

        expected_result = [
            { 'option': 'Partido 1', 'number': 1, 'votes': 24000, 'postproc': 10 },
            { 'option': 'Partido 4', 'number': 4, 'votes': 12000, 'postproc': 4 },
            { 'option': 'Partido 3', 'number': 3, 'votes': 8000, 'postproc': 3 },
            { 'option': 'Partido 6', 'number': 6, 'votes': 6000, 'postproc': 2 },
            { 'option': 'Partido 5', 'number': 5, 'votes': 4800, 'postproc': 1 },
            { 'option': 'Partido 2', 'number': 2, 'votes': 4000, 'postproc': 1 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
