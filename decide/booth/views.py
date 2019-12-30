import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_404_NOT_FOUND)
from base import mods
from django.contrib import auth
from census.models import Census
from voting.models import Voting
from django.shortcuts import render, redirect


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
        return None

class PageView(TemplateView):

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
