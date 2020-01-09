import django_filters.rest_framework
import codecs
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Voting, CandidatesGroup, Candidate
from .serializers import SimpleVotingSerializer, VotingSerializer
from base.perms import UserIsStaff
from base.models import Auth
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import UploadFileForm, NewVotingForm
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import requires_csrf_token
from django.db import transaction
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

import json
import csv
import os

dirspot = os.getcwd()

def findVotingByParam(request, voting):

    response = None
    votacion = None

    if type(voting) is int:
        votacion = Voting.objects.get(id=voting)
        response = HttpResponse("Es entero!")
    elif type(voting) is str:
        votacion = Voting.objects.get(custom_url=voting)
        response = HttpResponse("Es cadena!")

    return response

def candidates_load(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            validation_errors = handle_uploaded_file(request.FILES['file'])
            if len(validation_errors) > 0:
                return render(request, dirspot+'/voting/templates/upload.html', {'form': form, 'validation_errors': validation_errors})
            else:
                return HttpResponseRedirect('/admin/')
    else:
        form = UploadFileForm()
    return render(request, dirspot+'/voting/templates/upload.html', {'form': form})

def voting_edit(request):

    auths = Auth.objects.all()

    if request.method == 'POST':
        form = NewVotingForm(request.POST, request.FILES)

        votingName = request.POST["name"]
        votingDescription = request.POST["description"]

        
        permission_classes = (UserIsStaff,)
        #for data in ['name', 'desc', 'candidatures']:
        #    if not data in request.data:
        #        return Response({}, status=status.HTTP_400_BAD_REQUEST)

        if form.is_valid:
            candidatures = request.POST.getlist("candidatures")

            voting = Voting(name=votingName, desc=votingDescription)
                    #candidatures=request.data.get('candidatures'))
                    #question=question)
            voting.save()

            candidatures_db = []
            for candidature in candidatures:
                try:
                    c = CandidatesGroup.objects.get(name=candidature)
                    candidatures_db.append(c)
                except:
                    c = CandidatesGroup(name=candidature).save() 
                    candidatures_db.append(c)
            
            for cand in candidatures_db:
                voting.candidatures.add(cand)

            auths = request.POST.getlist("auths")
            auths_db = Auth.objects.all()
            auths_selected = []

            for at in auths_db:
                for ah in auths:
                    if at.name == ah:
                        auths_selected.append(at)

            for a in auths_selected:
                voting.auths.add(a)
            #Accion que se debe realizar en la lista
            #voting.create_pubkey()

        return render(request, dirspot+'/voting/templates/newVotingForm.html', {'status':status.HTTP_201_CREATED, 'auths':auths})
    else:
        form = NewVotingForm()
    return render(request, dirspot+'/voting/templates/newVotingForm.html', {'form': form, 'auths':auths})

@csrf_exempt
@transaction.atomic
def handle_uploaded_file(response):

    rows = response.POST['param'].split("\n")

    validation_errors = []
    provincias = ['VI', 'AB', 'A', 'AL', 'AV', 'BA', 'PM', 'B', 'BU', 'CC', 'CA', 'CS', 'CR', 'CO', 'C', 'CU', 'GI', 'GR', 'GU', 'SS', 'H', 'HU', 'J', 'LE', 
        'L', 'LO', 'LU', 'M', 'MA', 'MU', 'NA', 'OR', 'O', 'P', 'GC', 'PO', 'SA', 'TF', 'S', 'SG', 'SE', 'SO', 'T', 'TE', 'TO', 'V', 'VA', 'BI', 'ZA', 'Z', 'CE', 'ML']
    count_provincias = dict((prov, 0) for prov in provincias)
    provincias_variables = []
    
    row_line = 2
    candidatesGroupSex = {}
    count_presidents = {}
    for row in reader:
        name = dict(row).__getitem__('name')
        _type = dict(row).__getitem__('type')
        born_area = dict(row).__getitem__('born_area')
        current_area = dict(row).__getitem__('current_area')
        primaries = dict(row).__getitem__('primaries')
        sex = dict(row).__getitem__('sex')
        candidatesGroupName = dict(row).__getitem__('candidatesGroup')
        
        if sex == "HOMBRE":
            candidatesGroupSex[candidatesGroupName] = [candidatesGroupSex.get(candidatesGroupName, [0,0])[0] + 1, candidatesGroupSex.get(candidatesGroupName, [0,0])[1]]
        else:
            candidatesGroupSex[candidatesGroupName] = [candidatesGroupSex.get(candidatesGroupName, [0,0])[0], candidatesGroupSex.get(candidatesGroupName, [0,0])[1] + 1]
       
        if primaries == 'FALSE':
            primaries = False
            validation_errors.append("Error en la línea " + str(row_line) + ": El candidato " + str(name) + " no ha pasado el proceso de primarias")
        else:
            primaries = True

        if _type == "PRESIDENCIA":
            count_presidents[candidatesGroupName] = count_presidents.get(candidatesGroupName, 0) + 1
        else:
            count_presidents[candidatesGroupName] = count_presidents.get(candidatesGroupName, 0)

        try:
            CandidatesGroup.objects.get(name=candidatesGroupName)
        except:
            candidatesGroup_Search = CandidatesGroup(name=candidatesGroupName).save()

        if _type == 'CANDIDATO':
            if born_area in count_provincias and current_area in count_provincias:
                count_provincias[born_area] = count_provincias[born_area] + 1

            else:
                count_provincias[current_area] = count_provincias[current_area] + 1
                count_provincias[born_area] = count_provincias[born_area] + 1


        try:
            candidato = Candidate(name=name, type=_type, born_area=born_area, current_area=current_area, primaries= primaries, sex=sex, candidatesGroup=CandidatesGroup.objects.get(name=candidatesGroupName))
            candidato.full_clean()
        except ValidationError:
            validation_errors.append("Error en la línea " + str(row_line) + ": Hay errores de formato/validación")
        else:
            candidato.save()
        
        row_line = row_line + 1

        
    for key in count_presidents.keys():
        if count_presidents[key] > 1:
                validation_errors.append("La candidatura " + str(key) + " tiene más de un candidato a presidente")
    
    for key in candidatesGroupSex.keys():
        malePercentage = (candidatesGroupSex[key][0]*100)/(candidatesGroupSex[key][0]+candidatesGroupSex[key][1])
        if  malePercentage > 60 or malePercentage < 40:
            validation_errors.append("La candidatura " + str(key) + " no cumple un balance 60-40 entre hombres y mujeres")
        if candidatesGroupSex[key][0] + candidatesGroupSex[key][1] > 350:
            validation_errors.append("La candidatura " + str(key) + " supera el máximo de candidatos permitidos (350)")
    
    provincias_validacion = [prov for prov in provincias if count_provincias[prov] < 2]

    for prov in provincias_validacion:
        validation_errors.append("Tiene que haber al menos dos candidatos al congreso cuya provincia de nacimiento o de residencia tenga de código " + prov) 


    if len(validation_errors) > 0:
        transaction.set_rollback(True)
    
    return validation_errors


def voting_list(request):
    votings = Voting.objects.all()
    return render(request, "votings.html", {'votings':votings, 'STATIC_URL':settings.STATIC_URL})

def voting_list_update(request):
    voting_id = request.POST['voting_id']
    voting = get_object_or_404(Voting, pk=voting_id)
    action = request.POST['action']
    if action == 'start':
        if voting.start_date:
            url = "/admin/"
            # TODO Cuando seleccionas algunas que estan empezadas o no
        else:
            voting.start_date = timezone.now()
            voting.save()
            url = "/voting/votings/"
    elif action == 'stop':
        if not voting.start_date:
            url = "/admin/"
        elif voting.end_date:
            url = "/admin/"
        else:
            voting.end_date = timezone.now()
            voting.save()
            url = "/voting/votings/"
    elif action == 'tally':
        if not voting.start_date:
            url = "/admin/"
        elif not voting.end_date:
            url = "/admin/"
        elif voting.tally:
            url = "/admin/"
        else:
            voting.tally_votes(request.auth.key)
            url = "/voting/votings/"
    elif action == 'delete':
        voting.delete()
        url = "/voting/votings/"
    else:
        #TODO 
        url = "/voting/votings/"

    return HttpResponseRedirect(url)

def voting_list_update_multiple(request):
    array_voting_id = request.POST['array_voting_id[]'].split(",")
    action = request.POST['action_multiple']
    for voting_id in array_voting_id:
        voting = get_object_or_404(Voting, pk=voting_id)
        if action == 'start':
            if voting.start_date:
                url = "/admin/"
                # TODO Cuando seleccionas algunas que estan empezadas o no
            else:
                voting.start_date = timezone.now()
                voting.save()
                url = "/voting/votings/"
        elif action == 'stop':
            if not voting.start_date:
                url = "/admin/"
            elif voting.end_date:
                url = "/admin/"
            else:
                voting.end_date = timezone.now()
                voting.save()
                url = "/voting/votings/"
        elif action == 'tally':
            if not voting.start_date:
                url = "/admin/"
            elif not voting.end_date:
                url = "/admin/"
            elif voting.tally:
                url = "/admin/"
            else:
                #TODO
                voting.tally_votes(request.auth.key)
                url = "/voting/votings/"
        elif action == 'delete':
            #TODO 
            voting.delete()
            url = "/voting/votings/"
        else:
            #TODO 
            url = "/voting/votings/"

    return HttpResponseRedirect(url)

class VotingView(generics.ListCreateAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('id', )

    def get(self, request, *args, **kwargs):
        version = request.version
        if version not in settings.ALLOWED_VERSIONS:
            version = settings.DEFAULT_VERSION
        if version == 'v2':
            self.serializer_class = VotingSerializer

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        for data in ['name', 'desc', 'candidatures']:
            if not data in request.data:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        #question = Question(desc=request.data.get('question'))
        #question.save()
        #for idx, q_opt in enumerate(request.data.get('question_opt')):
        #    opt = QuestionOption(question=question, option=q_opt, number=idx)
        #    opt.save()
        voting = Voting(name=request.data.get('name'), desc=request.data.get('desc'),
                candidates=request.data.get('candidatures'))
                #question=question)
        voting.save()

        auth, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        auth.save()
        voting.auths.add(auth)

        return Response({}, status=status.HTTP_201_CREATED)


class VotingUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (UserIsStaff,)

    def put(self, request, voting_id, *args, **kwars):
        action = request.data.get('action')
        if not action:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        voting = get_object_or_404(Voting, pk=voting_id)
        msg = ''
        st = status.HTTP_200_OK
        if action == 'start':
            if voting.start_date:
                msg = 'Voting already started'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.start_date = timezone.now()
                voting.save()
                msg = 'Voting started'
        elif action == 'stop':
            if not voting.start_date:
                msg = 'Voting is not started'
                st = status.HTTP_400_BAD_REQUEST
            elif voting.end_date:
                msg = 'Voting already stopped'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.end_date = timezone.now()
                voting.save()
                msg = 'Voting stopped'
        elif action == 'tally':
            if not voting.start_date:
                msg = 'Voting is not started'
                st = status.HTTP_400_BAD_REQUEST
            elif not voting.end_date:
                msg = 'Voting is not stopped'
                st = status.HTTP_400_BAD_REQUEST
            elif voting.tally:
                msg = 'Voting already tallied'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.tally_votes(request.auth.key)
                msg = 'Voting tallied'
        else:
            msg = 'Action not found, try with start, stop or tally'
            st = status.HTTP_400_BAD_REQUEST
        return Response(msg, status=st)

def getVoting(request):
    id_voting = request.GET['id']
    voting = get_object_or_404(Voting, pk=id_voting)

    voting_json = VotingSerializer(voting)
    data = JSONRenderer().render(voting_json.data)
    return HttpResponse(data)

@csrf_exempt
def create_auth(request):
    name = request.POST["auth_name"]
    baseurl = request.POST["base_url"]
    auth_me = request.POST["auth_me"]

    if auth_me == 'True':
        me = True
    elif auth_me == 'False':
        me = False
    

    Auth.objects.get_or_create(url=baseurl, defaults={'me': me, 'name': name})

    auths = Auth.objects.all()
    
    return HttpResponse({'auths':auths})