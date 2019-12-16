import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from base import mods

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
        # Creamos el formulario de autenticación vacío
        form = UserCreationForm()
        if request.method == "POST":
            # Añadimos los datos recibidos al formulario
            form = UserCreationForm(data=request.POST)
            if form.is_valid():
                # Creamos la nueva cuenta de usuario
                user = form.save()

                # Si el usuario se crea correctamente 
                if user is not None:
                    do_login(request, user)
                    return redirect('/')

        return render(request, "booth/register.html", {'form': form})

    def login(request):
        form = AuthenticationForm()
        if request.method == "POST":
            # Añadimos los datos recibidos al formulario
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                # Recuperamos las credenciales validadas
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                # Verificamos las credenciales del usuario
                user = authenticate(request, username=username, password=password)
                print(user)
                # Si existe un usuario con ese nombre y contraseña
                if user is not None:
                    do_login(request, user)
                    return redirect('/')

        return render(request, "booth/login.html", {'form': form})

    def logout(request):
        do_logout(request)
        return redirect('/')