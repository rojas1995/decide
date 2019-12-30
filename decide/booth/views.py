import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
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

# TODO: check permissions and census
class BoothView(TemplateView):
    template_name = 'booth/booth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})

            # Casting numbers to string to manage in javascript with BigInt
            # and avoid problems with js and big number conversion
            for k, v in r[0]['pub_key'].items():
                r[0]['pub_key'][k] = str(v)

            context['voting'] = json.dumps(r[0])
        except:
            raise Http404

        context['KEYBITS'] = settings.KEYBITS

        return context


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

        if request.method == "POST":
            # Recuperamos las credenciales validadas
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Verificamos las credenciales del usuario
            user = authenticate(request, username=username, password=password)
            print(user)
            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                do_login(request, user)
                return redirect('/')

        return render(request, "booth/login.html")

    def logout(request):
        do_logout(request)
        return redirect('/')

    def llamarIndex(request):
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
