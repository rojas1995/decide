import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_404_NOT_FOUND)
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
