import json, requests
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
from voting.models import Voting
from store.models import Vote
from django.shortcuts import render, redirect
from Crypto.Random import random
from rest_framework.authtoken.models import Token
from django.utils import timezone


def booth(request, **kwargs):
    if request.method == 'GET':
        try:
            voting_id = kwargs.get('voting_id')
            if voting_checks(voting_id):
                voting = Voting.objects.get(pk = voting_id)
                return render(request, 'booth/booth.html', {'voting': voting})
            else:
                raise Http404
        except:
            raise Http404
    if request.method == 'POST':
        try:
            voting_id = kwargs.get('voting_id')
            if voting_checks(voting_id):
                voting = Voting.objects.get(pk = voting_id)
                option = int(request.POST['option'])
                user_id = request.user.id
                token = str(Token.objects.get(user = request.user))

                bigpk = {
                        'p': str(voting.pub_key.p),
                        'g': str(voting.pub_key.g),
                        'y': str(voting.pub_key.y),
                    }
                
                vote = encrypt(bigpk, option)

                send_data(request, user_id, token, voting_id, vote)
                
                return render(request, 'booth/success.html', {'user': request.user})
            else:
                raise Http404
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

        for c in census:
            voting_id = c.voting_id
            # Only for list view
            try:
                if voting_id is not None and voting_checks(voting_id):
                    voting = Voting.objects.get(pk = voting_id)
                    res.append(voting)
            except Voting.DoesNotExist:
                pass

        return render(request, 'booth/votinglist.html', {'res':res})
    else:
        #If user is not log in, redirect to log in page.
        return PageView.login(request)
        

class PageView(TemplateView):

    def register(request):
        if request.user.is_authenticated:
            return redirect('/')
            
        form = None
        password = 0
        if request.method == "POST":
            form = registerForm(request.POST)
            if form.is_valid():
                if request.POST.get('password') == request.POST.get('confirm_password'):
                    user = form.save()
                    user.set_password(form.cleaned_data['password'])
                    user.save()

                    # Si el usuario se crea correctamente 
                    if user is not None:
                        return redirect('/login')
                else:
                    password = 1

        return render(request, "booth/register.html", {'form': form, 'password': password})

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
                return redirect('/')
            else:
                errors = 1
        return render(request, "booth/login.html", {'errors': errors})

    def logout(request):
        do_logout(request)
        return redirect('/')

    def index(request):
        return render(request, 'booth/index.html')
    
    def profile(request):
        print(request)
        return render(request, 'booth/profile.html')


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


def check_date(date):
    today = timezone.now()
    if date > today:
        # If voting end_date is before today:
        return True
    else:
        return False

def voting_checks(voting_id):
    aux = False
    voting = Voting.objects.get(pk = voting_id)
    # Check dates. Voting must be between stablished dates
    if (voting.end_date is None or check_date(voting.end_date)) and (voting.start_date is None or not check_date(voting.start_date)):
        # Check that voter doesn't send other vote to this voting
        try:
            Vote.objects.get(voting_id = voting_id)
        except Vote.DoesNotExist:
            aux = True
    return aux
