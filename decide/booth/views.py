import json, httplib2
import requests
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_404_NOT_FOUND)
from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from base import mods
from booth.form import registerForm
from django.contrib import auth
from census.models import Census
from voting.models import Voting, Question, QuestionOption
from django.shortcuts import render, redirect
from Crypto.Random import random
from rest_framework.authtoken.models import Token

# TODO: check permissions and census

def booth(request, **kwargs):
    if request.method == 'GET':
        try:
            voting_id = kwargs.get('voting_id')
            voting = Voting.objects.get(pk = voting_id)

            return render(request, 'booth/booth.html', {'voting': voting})
        except:
            raise Http404
    if request.method == 'POST':
        try:
            voting_id = kwargs.get('voting_id')
            voting = Voting.objects.get(pk = voting_id)
            option = int(request.POST['option'])
            user_id = request.user.id
            token = str(Token.objects.get(user = request.user))#Necesitamos que en el request este el auth

            bigpk = {
                    'p': str(voting.pub_key.p),
                    'g': str(voting.pub_key.g),
                    'y': str(voting.pub_key.y),
                }

            vote = encrypt(bigpk, option)

            send_data(request, user_id, token, voting_id, vote)
            

            return render(request, 'booth/success.html', {'user': request.username})
        except:
            raise Http404


def send_data(request, user, token, voting, vote):
    data = json.dumps({
            'voter': user,
            'token': token,
            'voting': voting,
            'vote': {'a': str(vote[0]), 'b': str(vote[1])}
        })

    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Token ' + token
    }

    r = requests.post(url = 'http://' + request.META['HTTP_HOST']+ '/gateway/store/', data = data, headers = headers)
    return r
    

def encrypt(pk, M):
    k = random.StrongRandom().randint(1, int(pk["p"]) - 1)
    a = pow(int(pk["g"]), k, int(pk["p"]))
    b = (pow(int(pk["y"]), k, int(pk["p"])) * M) % int(pk["p"])
    return a, b

def votinglist(request):
    user_id = request.user.id

    if user_id is not None:
        census = Census.objects.filter(voter_id=user_id)
        res = []
        for censu in census:
            voto_id = censu.voting_id
            voting = Voting.objects.get(pk = voto_id)
            res.append(voting)
        return render(request, 'booth/votinglist.html', {'res':res})
    else:
        #If user is not log in, redirect to log in page.
        return PageView.login(request)

class PageView(TemplateView):

    def register(request):
        if request.user.is_authenticated:
            return redirect('/')
            
        form = None
        if request.method == "POST":
            form = registerForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.set_password(form.cleaned_data['password'])
                user.save()

                # Si el usuario se crea correctamente 
                if user is not None:
                    return redirect('/login')

        return render(request, "booth/register.html", {'form': form})

    def login(request):
        if request.user.is_authenticated:
            return redirect('/')

        errors = 0
        if request.method == "POST":
            # Recuperamos las credenciales validadas
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Verificamos las credenciales del usuario
            user = authenticate(request, username=username, password=password)
            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                do_login(request, user)
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                errors = 1
        return render(request, "booth/login.html", {'errors': errors})

    def logout(request):
        do_logout(request)
        return redirect('/')


    def index(request):
        return render(request, 'booth/index.html')

class GetVoting(APIView):
    def post(self, request):
        vid = request.data.get('voting', '')
        try:
            r = mods.get('voting', params={'id': vid})
            for k, v in r[0]['pub_key'].items():
                r[0]['pub_key'][k] = str(v)
            return Response(r[0], status=HTTP_200_OK)
        except:
            return Response({}, status=HTTP_404_NOT_FOUND)
