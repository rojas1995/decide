import random
import itertools
import re
import os
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods
from base.tests import BaseTestCase
from census.models import Census
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption, Candidate
from voting.views import handle_uploaded_file
import unittest
from selenium import webdriver

class VotingTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_voting_gobern(self):
        print("Creando Votación Presidenciales - Congreso")
        v = Voting(name="Votación Gobierno 2020")
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    #def create_voting(self):
    #    q = Question(desc='test question')
    #    q.save()
    #    for i in range(5):
    #        opt = QuestionOption(question=q, option='option {}'.format(i+1))
    #        opt.save()
    #    v = Voting(name='test voting', question=q)
    #    v.save()

    #    a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
    #                                      defaults={'me': True, 'name': 'test auth'})
    #    a.save()
    #    v.auths.add(a)

    #    return v

    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

    def store_votes(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        clear = {}
        for opt in v.question.options.all():
            clear[opt.number] = 0
            for i in range(random.randint(0, 5)):
                a, b = self.encrypt_msg(opt.number, v)
                data = {
                    'voting': v.id,
                    'voter': voter.voter_id,
                    'vote': { 'a': a, 'b': b },
                }
                clear[opt.number] += 1
                user = self.get_or_create_user(voter.voter_id)
                self.login(user=user.username)
                voter = voters.pop()
                mods.post('store', json=data)
        return clear

    def test_complete_voting(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes(v)

        self.login()  # set token
        v.tally_votes(self.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])

    def test_create_voting_from_api(self):
        data = {'name': 'Example'}
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse']
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_voting(self):
        voting = self.create_voting()

        data = {'action': 'start'}
        #response = self.client.post('/voting/{}/'.format(voting.pk), data, format='json')
        #self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        data = {'action': 'bad'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)

        # STATUS VOTING: not started
        for action in ['stop', 'tally']:
            data = {'action': action}
            response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), 'Voting is not started')

        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting started')

        # STATUS VOTING: started
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting is not stopped')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting stopped')

        # STATUS VOTING: stopped
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting tallied')

        # STATUS VOTING: tallied
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already tallied')

    def csv_validation_primaries_test(self):
        num_candidatos_inicial = len(Candidate.objects.all())

        path = str(os.getcwd()) + "/voting/files/candidatos-test-primarias.csv"
        file = open(path, 'rb')
        errores_validacion = handle_uploaded_file(file)
        lista_comprobacion = list(filter(re.compile(r'no ha pasado el proceso de primarias').search, errores_validacion))
        print(lista_comprobacion)
        num_candidatos_final = len(Candidate.objects.all())
        self.assertTrue(len(lista_comprobacion) == 1 and num_candidatos_inicial == num_candidatos_final)

    def csv_validation_genres_test(self):
        num_candidatos_inicial = len(Candidate.objects.all())
        path = str(os.getcwd()) + "/voting/files/candidatos-test-genero.csv"
        file = open(path, 'rb')
        errores_validacion = list(filter(re.compile(r'no cumple un balance 60-40 entre hombres y mujeres')
        .search, handle_uploaded_file(file)))
        list_expected_candidates_group = ["BETIS","MALAGA","BARCELONA"]
        list_received_candidates_group = []
        for error in errores_validacion:
            candidatura = error.split(" no cumple")[0].split("candidatura ")[1]
            list_received_candidates_group.append(str(candidatura))
        num_candidatos_final = len(Candidate.objects.all())
        self.assertTrue(set(list_expected_candidates_group).issuperset(list_received_candidates_group)
         and len(list_received_candidates_group) == len(list_expected_candidates_group)
          and num_candidatos_inicial == num_candidatos_final)
    
    def csv_validation_maximum_candidates_test(self):
        num_candidatos_inicial = len(Candidate.objects.all())
        path = str(os.getcwd()) + "/voting/files/candidatos-test-maximo.csv"
        file = open(path, 'rb')
        errores_validacion = list(filter(re.compile(r'supera el máximo de candidatos permitidos')
        .search, handle_uploaded_file(file)))
        list_expected_candidates_group = ["SEVILLA", "BETIS"]
        list_received_candidates_group = []
        for error in errores_validacion:
            candidatura = error.split(" supera el")[0].split("candidatura ")[1]
            list_received_candidates_group.append(str(candidatura))
        num_candidatos_final = len(Candidate.objects.all())
        self.assertTrue(set(list_expected_candidates_group).issuperset(list_received_candidates_group)
         and len(list_received_candidates_group) == len(list_expected_candidates_group)
          and num_candidatos_inicial == num_candidatos_final)
    
    def csv_validation_provincias_test(self):
        num_candidatos_inicial = len(Candidate.objects.all())

        path = str(os.getcwd()) + "/voting/files/candidatos-test-provincias.csv"
        file = open(path, 'rb')
        errores_validacion = handle_uploaded_file(file)
        lista_comprobacion = list(filter(re.compile(r'Tiene que haber al menos dos candidatos al congreso cuya provincia de nacimiento o de residencia tenga de código ML').search, errores_validacion))
        print(lista_comprobacion)
        num_candidatos_final = len(Candidate.objects.all())
        self.assertTrue(len(lista_comprobacion) == 1 and num_candidatos_inicial == num_candidatos_final)

    def csv_validation_presidents_test(self):
            num_candidatos_inicial = len(Candidate.objects.all())
            path = str(os.getcwd()) + "/voting/files/candidatos-test-presidents.csv"
            file = open(path, 'rb')
            errores_validacion = list(filter(re.compile(r'tiene más de un candidato a presidente')
            .search, handle_uploaded_file(file)))
            list_expected_candidates_group = ["MALAGA"]
            list_received_candidates_group = []
            for error in errores_validacion:
                candidatura = error.split(" tiene más")[0].split("candidatura ")[1]
                list_received_candidates_group.append(str(candidatura))
            num_candidatos_final = len(Candidate.objects.all())
            self.assertTrue(set(list_expected_candidates_group).issuperset(list_received_candidates_group)
            and len(list_received_candidates_group) == len(list_expected_candidates_group)
            and num_candidatos_inicial == num_candidatos_final)

class TestSignup(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        
    def test_custom_url(self):
        self.driver.get("http://localhost:8000/admin/login/?next=/admin/")
        # TODO
        self.driver.find_element_by_id('id_username').send_keys("practica")
        self.driver.find_element_by_id('id_password').send_keys("practica")
        #self.driver.find_element_by_id('login-form').click()
        #self.assertTrue(len(self.driver.find_elements_by_id('user-tools'))>0) 
    
    def tearDown(self):
        self.driver.quit

if __name__ == '__main__':
    unittest.main()