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


    def test_paridad1(self):
        data = {
            'type': 'DHONDTP',
            'seats': 12,
            'options': [
                { 'option': 'Partido 1', 'number': 1, 'votes': 50 , 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
                { 'option': 'Partido 2', 'number': 2, 'votes': 10, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
                { 'option': 'Partido 3', 'number': 3, 'votes': 34, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
                { 'option': 'Partido 4', 'number': 4, 'votes': 25, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ] },
                { 'option': 'Partido 5', 'number': 5, 'votes': 56, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
                { 'option': 'Partido 6', 'number': 6, 'votes': 170, 'candidatos': [
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

    def test_paridad2(self):
        data = {
            'type': 'DHONDTP',
            'seats': 17,
            'options': [
                { 'option': 'Partido 6', 'number': 6, 'votes': 1000000, 'candidatos': [
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
                { 'option': 'Partido 5', 'number': 5, 'votes': 56, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
                { 'option': 'Partido 1', 'number': 1, 'votes': 50, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
                { 'option': 'Partido 3', 'number': 3, 'votes': 34, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ] },
                { 'option': 'Partido 4', 'number': 4, 'votes': 25, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
                { 'option': 'Partido 2', 'number': 2, 'votes': 10, 'candidatos': [
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
                { 'option': 'Partido 5', 'number': 5, 'votes': 56, 'postproc': 0, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ],'paridad': []},
                { 'option': 'Partido 1', 'number': 1, 'votes': 50, 'postproc': 0, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ],'paridad':[]},
                { 'option': 'Partido 3', 'number': 3, 'votes': 34, 'postproc': 0, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ], 'paridad':[]},
                { 'option': 'Partido 4', 'number': 4, 'votes': 25, 'postproc': 0, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ], 'paridad':[]},
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

    def test_dhondt6(self):
        data = {
            'type': 'DHONDT',
            'seats': 21,
            'options': [
                { 'option': 'Partido 1', 'number': 1, 'votes': 5500 },
                { 'option': 'Partido 2', 'number': 2, 'votes': 5500 },
                { 'option': 'Partido 3', 'number': 3, 'votes': 10000 },
                { 'option': 'Partido 4', 'number': 4, 'votes': 5000 },
                { 'option': 'Partido 5', 'number': 5, 'votes': 5000 },
                { 'option': 'Partido 6', 'number': 6, 'votes': 5000 },
                { 'option': 'Partido 7', 'number': 7, 'votes': 5000 },
                { 'option': 'Partido 8', 'number': 8, 'votes': 5000 },
                { 'option': 'Partido 9', 'number': 9, 'votes': 5000 },
                { 'option': 'Partido 10', 'number': 10, 'votes': 5000 },
                { 'option': 'Partido 11', 'number': 11, 'votes': 5000 },
                { 'option': 'Partido 12', 'number': 12, 'votes': 5000 },
                { 'option': 'Partido 13', 'number': 13, 'votes': 5000 },
                { 'option': 'Partido 14', 'number': 14, 'votes': 5000 },
                { 'option': 'Partido 15', 'number': 15, 'votes': 5000 },
                { 'option': 'Partido 16', 'number': 16, 'votes': 5000 },
                { 'option': 'Partido 17', 'number': 17, 'votes': 5000 },
            ]
        }

        expected_result = [
            { 'option': 'Partido 3', 'number': 3, 'votes': 10000, 'postproc': 3 },
            { 'option': 'Partido 1', 'number': 1, 'votes': 5500, 'postproc': 2 },
            { 'option': 'Partido 2', 'number': 2, 'votes': 5500, 'postproc': 2 },
            { 'option': 'Partido 4', 'number': 4, 'votes': 5000, 'postproc': 1 },
            { 'option': 'Partido 5', 'number': 5, 'votes': 5000, 'postproc': 1 },
            { 'option': 'Partido 6', 'number': 6, 'votes': 5000, 'postproc': 1 },
            { 'option': 'Partido 7', 'number': 7, 'votes': 5000, 'postproc': 1 },
            { 'option': 'Partido 8', 'number': 8, 'votes': 5000, 'postproc': 1 },
            { 'option': 'Partido 9', 'number': 9, 'votes': 5000, 'postproc': 1 },
            { 'option': 'Partido 10', 'number': 10, 'votes': 5000, 'postproc': 1 },
            { 'option': 'Partido 11', 'number': 11, 'votes': 5000, 'postproc': 1 },
            { 'option': 'Partido 12', 'number': 12, 'votes': 5000, 'postproc': 1 },
            { 'option': 'Partido 13', 'number': 13, 'votes': 5000, 'postproc': 1 },
            { 'option': 'Partido 14', 'number': 14, 'votes': 5000, 'postproc': 1 },
            { 'option': 'Partido 15', 'number': 15, 'votes': 5000, 'postproc': 1 },
            { 'option': 'Partido 16', 'number': 16, 'votes': 5000, 'postproc': 1 },
            { 'option': 'Partido 17', 'number': 17, 'votes': 5000, 'postproc': 1 },
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


    def test_dhondt7(self):
        data = {
            'type': 'DHONDT',
            'seats': 20,
            'options': [
                { 'option': 'Partido 1', 'number': 1, 'votes': 1 },
                { 'option': 'Partido 2', 'number': 2, 'votes': 0 },
                { 'option': 'Partido 3', 'number': 3, 'votes': 0 },
                { 'option': 'Partido 4', 'number': 4, 'votes': 0 },
            ]
        }

        expected_result = [
            { 'option': 'Partido 1', 'number': 1, 'votes': 1, 'postproc': 20 },
            { 'option': 'Partido 2', 'number': 2, 'votes': 0, 'postproc': 0 },
            { 'option': 'Partido 3', 'number': 3, 'votes': 0, 'postproc': 0 },
            { 'option': 'Partido 4', 'number': 4, 'votes': 0, 'postproc': 0 },
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

    def test_dhondt8(self):
        data = {
            'type': 'DHONDT',
            'seats': 7,
            'options': [
                { 'option': 'Partido 1', 'number': 1, 'votes': 1000 },
            ]
        }

        expected_result = [
            { 'option': 'Partido 1', 'number': 1, 'votes': 1000, 'postproc': 7 },
            
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def test_paridad3(self):
        data = {
            'type': 'DHONDTP',
            'seats': 12,
            'options': [
                { 'option': 'Partido 1', 'number': 1, 'votes': 50 , 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'hombre','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
                { 'option': 'Partido 2', 'number': 2, 'votes': 10, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'mujer','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'mujer','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
                { 'option': 'Partido 3', 'number': 3, 'votes': 34, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
                { 'option': 'Partido 4', 'number': 4, 'votes': 25, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ] },
                { 'option': 'Partido 5', 'number': 5, 'votes': 56, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
                { 'option': 'Partido 6', 'number': 6, 'votes': 170, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
            ]
        }
        expected_result = {'message' : 'la diferencia del numero de hombres y mujeres es de más de un 60% - 40%'}

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_paridad4(self):
        data = {
            'type': 'SIMPLESP',
            'seats':7,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5,  'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]}, 
                { 'option': 'Option 2', 'number': 2, 'votes': 0,'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
                { 'option': 'Option 3', 'number': 3, 'votes': 3, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]}, 
                { 'option': 'Option 4', 'number': 4, 'votes': 2,'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ] },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 ,'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
                { 'option': 'Option 6', 'number': 6, 'votes': 1 ,'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ]},
        
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 2, 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ], 
                'paridad': [
                {'sexo':'mujer','id':'2'},
                {'sexo':'hombre','id':'1'}
                ]
            },
              
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 2 , 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ], 
                'paridad': [
                {'sexo':'mujer','id':'2'},
                {'sexo':'hombre','id':'1'}
                ]
            },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 1 , 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ], 
                'paridad': [
                {'sexo':'mujer','id':'2'}
                ]
            },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 1 , 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ], 
                'paridad': [
                {'sexo':'hombre','id':'1'}
                ]
            },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 , 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ], 
                'paridad': [
                {'sexo':'mujer','id':'2'}
                ]
            },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 , 'candidatos': [
                 {'sexo':'hombre','id':'1'}
                ,{'sexo':'mujer','id':'2'}
                ,{'sexo':'hombre','id':'3'}
                ,{'sexo':'mujer','id':'4'}
                ,{'sexo':'hombre','id':'5'}
                ,{'sexo':'mujer','id':'6'}
                ], 
                'paridad': []}
        }

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)