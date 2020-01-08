import django_filters.rest_framework
import codecs
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


import csv
import os

def candidates_load(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/admin/')
    else:
        form = UploadFileForm()
    return render(request, dirspot+'/voting/templates/upload.html', {'form': form})

def voting_edit(request):

    if request.method == 'POST':
        form = NewVotingForm(request.POST, request.FILES)
        
        votingName = request.POST["name"]
        votingDescription = request.POST["description"]

        files = request.FILES.getlist('file_field')
        print(files)
        permission_classes = (UserIsStaff,)
        #for data in ['name', 'desc', 'candidatures']:
        #    if not data in request.data:
        #        return Response({}, status=status.HTTP_400_BAD_REQUEST)

        if form.is_valid:
            candidatures = []
            for f in files:
                candidature = handle_file(f)
                candidatures.append(candidature)

        voting = Voting(name=votingName, desc=votingDescription)
                #candidatures=request.data.get('candidatures'))
                #question=question)
        voting.save()

        voting.candidatures.set(candidatures)

        auth, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        auth.save()
        voting.auths.add(auth)

        return render(request, dirspot+'/voting/templates/newVotingForm.html', {'status':status.HTTP_201_CREATED})
    else:
        form = NewVotingForm()
    return render(request, dirspot+'/voting/templates/newVotingForm.html', {'form': form})


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

    for row in rows:
        user = row.split("#")
        if user[0] != '':
            name = user[0]
            _type = user[1]
            born_area = user[2]
            current_area = user[3]
            primaries = user[4]
            sex = user[5]
            candidatesGroupName = user[6]
            
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

            if _type == 'CANDIDATO':
                if born_area in count_provincias and current_area in count_provincias:
                    count_provincias[born_area] = count_provincias[born_area] + 1

                else:
                    count_provincias[current_area] = count_provincias[current_area] + 1
                    count_provincias[born_area] = count_provincias[born_area] + 1

            try:
                CandidatesGroup.objects.get(name=candidatesGroupName)
            except:
                CandidatesGroup(name=candidatesGroupName).save()

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

    return HttpResponse(validation_errors)
    #return validation_errors



def handle_file(f):
    reader = csv.DictReader(codecs.iterdecode(f, 'utf-8'), delimiter="#")
    candidature = ""
    for row in reader:
        print(row)
        name = dict(row).__getitem__('name')
        _type = dict(row).__getitem__('type')
        born_area = dict(row).__getitem__('born_area')
        current_area = dict(row).__getitem__('current_area')
        primaries = dict(row).__getitem__('primaries')
        sex = dict(row).__getitem__('sex')
        candidatesGroupName = dict(row).__getitem__('candidatesGroup')
        
        if primaries == 'FALSE':
            primaries = False
        else:
            primaries = True

        try:
            candidature = CandidatesGroup.objects.get(name=candidatesGroupName)
        except:
            candidature = CandidatesGroup(name=candidatesGroupName).save()
        
        Candidate(name=name, type=_type, born_area=born_area, current_area=current_area, primaries= primaries, sex=sex, candidatesGroup=CandidatesGroup.objects.get(name=candidatesGroupName)).save()
    
    return candidature

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

