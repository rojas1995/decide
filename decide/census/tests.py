import random
from unittest import skip, skipIf

import pytest
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Census
from voting.models import Voting
from base import mods

from base.tests import BaseTestCase


class CensusTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.census = Census(voting_id=1, voter_id=1)
        self.census.save()

    def tearDown(self):
        super().tearDown()
        self.census = None

    def test_check_vote_permissions(self):
        response = self.client.get('/census/{}/?voter_id={}'.format(1, 2), format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 'Invalid voter')

        response = self.client.get('/census/{}/?voter_id={}'.format(1, 1), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Valid voter')

    def test_list_voting(self):
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'voters': [1]})

    def test_add_new_voters_conflict(self):
        data = {'voting_id': 1, 'voters': [1]}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 409)

    def test_add_new_voters(self):
        data = {'voting_id': 2, 'voters': [1, 2, 3, 4]}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(data.get('voters')), Census.objects.count() - 1)

    def test_destroy_voter(self):
        data = {'voters': [1]}
        response = self.client.delete('/census/{}/'.format(1), data, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(0, Census.objects.count())

    def test_census_driver(self):
        self.login()
        # username, password1, password2, nombre, apellido, email, edad, sexo, municipio, votación, status_code
        user_data = [
            ['username1', 'abcd1234', 'abcd1234', 'nombre1', 'apellido1', 'correo1@mail.com', '21', 'Masculino',
             'Sevilla', 'votaciontest1', 201],
            ['username2', 'abcd1234', 'abcd1234', 'nombre2', 'apellido2', 'correo2@mail.com', '22', 'Femenino',
             'Sevilla', 'votaciontest2', 201]
        ]
        for data in user_data:
            self._census_create(*data)

    def _census_create(self, username, password1, password2, nombre, apellido, email, sexo, edad, municipio,
                       votacion, expected_status_code):

        found_status = 302

        # /admin/auth/user/add/ -- Crear al nuevo usuario/Registrarse en la app
        user_acc = {'username': username,
                    'password1': password1,
                    'password2': password2}
        response = self.client.post('/admin/auth/user/add/', user_acc, format='json')
        self.assertEqual(response.status_code, expected_status_code)

        # Traemos el usuario creado
        user_id = User.objects.filter(username=username).values('id')[0]['id']

        # /admin/auth/user/{id_voter}/change/ -- Editar datos del usuario
        user_data = {'username': username,
                     'first_name': nombre,
                     'last_name': apellido,
                     'email': email}
        response = self.client.get('/admin/auth/user/{}/change/'.format(user_id))
        self.assertEqual(response.status_code, found_status)
        response = self.client.post('/admin/auth/user/{}/change/'.format(user_id), user_data, format='json')
        self.assertEqual(response.status_code, expected_status_code)

        # /admin/authentication/perfil/{id_voter}/change/ -- Editar el perfil del usuario
        user_profile = {'user': username,
                        'sexo': sexo,
                        'edad': edad,
                        'municipio': municipio}
        response = self.client.get('/admin/authentication/perfil/{}/change/'.format(user_id))
        self.assertEqual(response.status_code, found_status)
        response = self.client.post('/admin/authentication/perfil/{}/change/'.format(user_id),
                                    user_profile, format='json')
        self.assertEqual(response.status_code, expected_status_code)

        # admin/voting/voting/add/ -- Crear la votacion
        voting_data = {
            'name': votacion,
            'desc': 'descripcion de la votacion de test',
            'question': 'la pregunta de la votacion de test',
            'question_opt': ['verdadero', 'falso', 'nada es lo que parece']
        }
        response = self.client.post('/voting/', voting_data, format='json')
        self.assertEqual(response.status_code, 201)

        # Traemos la votacion creada
        voting_id = Voting.objects.filter(name=votacion).values('id')[0]['id']

        # /admin/census/census/add/ -- Añadir usuarios al censo
        census_data = {'voting_id': voting_id,
                       'voters': user_id}
        response = self.client.post('/admin/census/census/add/', census_data, format='json')
        self.assertEqual(response.status_code, expected_status_code)

        # /census/web/ -- Comprueba que los datos nuevo esten en la vista
        response = self.client.post('/census/web/')
        self.assertIn(nombre, response.content)
        self.assertIn(apellido, response.content)
        self.assertIn(municipio, response.content)
