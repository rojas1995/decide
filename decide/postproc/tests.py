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

    def test_paridad1(self):
        data = {
            'type': 'PARIDAD',
            'seats': 12,
            'options': [
                { 'option': 'Partido 6', 'number': 6, 'votes': 170, 'postproc': 6, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
                { 'option': 'Partido 5', 'number': 5, 'votes': 56, 'postproc': 2, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
                { 'option': 'Partido 1', 'number': 1, 'votes': 50, 'postproc': 2, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
                { 'option': 'Partido 3', 'number': 3, 'votes': 34, 'postproc': 1, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ] },
                { 'option': 'Partido 4', 'number': 4, 'votes': 25, 'postproc': 1, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
                { 'option': 'Partido 2', 'number': 2, 'votes': 10, 'postproc': 0, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
            ]
        }

        expected_result = [{ 'option': 'Partido 6', 'number': 6, 'votes': 170, 'postproc': 6, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ], 
                'paridad': [
                {'sexo':'mujer','id':'2'},
                {'sexo':'hombre','id':'1'},
                {'sexo':'mujer','id':'4'},
                {'sexo':'hombre','id':'3'},
                {'sexo':'mujer','id':'6'},
                {'sexo':'hombre','id':'5'}
                ]
                },
                { 'option': 'Partido 5', 'number': 5, 'votes': 56, 'postproc': 2, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ],'paridad': [
                {'sexo':'mujer','id':'2'},
                {'sexo':'hombre','id':'1'}]},
                { 'option': 'Partido 1', 'number': 1, 'votes': 50, 'postproc': 2, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ],'paridad':[
                {'sexo':'mujer','id':'2'},
                {'sexo':'hombre','id':'1'}]},
                { 'option': 'Partido 3', 'number': 3, 'votes': 34, 'postproc': 1, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ], 'paridad':[
                {'sexo':'mujer','id':'2'}]},
                { 'option': 'Partido 4', 'number': 4, 'votes': 25, 'postproc': 1, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ], 'paridad':[
                {'sexo':'mujer','id':'2'}]},
                { 'option': 'Partido 2', 'number': 2, 'votes': 10, 'postproc': 0, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ], 'paridad':[]}
            ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_paridad2(self):
        data = {
            'type': 'PARIDAD',
            'seats': 17,
            'options': [
                { 'option': 'Partido 6', 'number': 6, 'votes': 1000000, 'postproc': 17, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ,{'sexo':'hombre','id':'7'}
                ,{'sexo':'mujer','id':'8'}
                ,{'sexo':'hombre','id':'9'}
                ,{'sexo':'mujer','id':'10'}
                ,{'sexo':'hombre','id':'11'}
                ,{'sexo':'mujer','id':'12'}
                ,{'sexo':'hombre','id':'13'}
                ,{'sexo':'mujer','id':'14'}
                ,{'sexo':'hombre','id':'15'}
                ,{'sexo':'mujer','id':'16'}
                ,{'sexo':'hombre','id':'17'}
                ,{'sexo':'mujer','id':'18'}
                ]},
                { 'option': 'Partido 5', 'number': 5, 'votes': 56, 'postproc': 0, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
                { 'option': 'Partido 1', 'number': 1, 'votes': 50, 'postproc': 0, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
                { 'option': 'Partido 3', 'number': 3, 'votes': 34, 'postproc': 0, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ] },
                { 'option': 'Partido 4', 'number': 4, 'votes': 25, 'postproc': 0, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
                { 'option': 'Partido 2', 'number': 2, 'votes': 10, 'postproc': 0, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
            ]
        }

        expected_result = [{ 'option': 'Partido 6', 'number': 6, 'votes': 1000000, 'postproc': 17, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ,{'sexo':'hombre','id':'7'}
                ,{'sexo':'mujer','id':'8'}
                ,{'sexo':'hombre','id':'9'}
                ,{'sexo':'mujer','id':'10'}
                ,{'sexo':'hombre','id':'11'}
                ,{'sexo':'mujer','id':'12'}
                ,{'sexo':'hombre','id':'13'}
                ,{'sexo':'mujer','id':'14'}
                ,{'sexo':'hombre','id':'15'}
                ,{'sexo':'mujer','id':'16'}
                ,{'sexo':'hombre','id':'17'}
                ,{'sexo':'mujer','id':'18'}
                ], 
                'paridad': [
                {'sexo':'mujer','id':'2'},
                {'sexo':'hombre','id':'1'},
                {'sexo':'mujer','id':'4'},
                {'sexo':'hombre','id':'3'},
                {'sexo':'mujer','id':'6'},
                {'sexo':'hombre','id':'5'},
                {'sexo':'mujer','id':'8'},
                {'sexo':'hombre','id':'7'},
                {'sexo':'mujer','id':'10'},
                {'sexo':'hombre','id':'9'},
                {'sexo':'mujer','id':'12'},
                {'sexo':'hombre','id':'11'},
                {'sexo':'mujer','id':'14'},
                {'sexo':'hombre','id':'13'},
                {'sexo':'mujer','id':'16'},
                {'sexo':'hombre','id':'15'},
                {'sexo':'mujer','id':'18'},
                ]
                },
                { 'option': 'Partido 5', 'number': 5, 'votes': 56, 'postproc': 2, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ],'paridad': [
                {'sexo':'mujer','id':'2'},
                {'sexo':'hombre','id':'1'}]},
                { 'option': 'Partido 1', 'number': 1, 'votes': 50, 'postproc': 2, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ],'paridad':[
                {'sexo':'mujer','id':'2'},
                {'sexo':'hombre','id':'1'}]},
                { 'option': 'Partido 3', 'number': 3, 'votes': 34, 'postproc': 1, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ], 'paridad':[
                {'sexo':'mujer','id':'2'}]},
                { 'option': 'Partido 4', 'number': 4, 'votes': 25, 'postproc': 1, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ], 'paridad':[
                {'sexo':'mujer','id':'2'}]},
                { 'option': 'Partido 2', 'number': 2, 'votes': 10, 'postproc': 0, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ], 'paridad':[]}
            ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)