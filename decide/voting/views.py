import django_filters.rest_framework
import codecs
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Question, QuestionOption, Voting, CandidatesGroup, Candidate
from .serializers import SimpleVotingSerializer, VotingSerializer
from base.perms import UserIsStaff
from base.models import Auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from django.db import transaction
from django.core.exceptions import ValidationError

import csv
import os
dirspot = os.getcwd()
print(dirspot)
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

@transaction.atomic
def handle_uploaded_file(f):
    reader = csv.DictReader(codecs.iterdecode(f, 'utf-8'), delimiter="#")
    
    validation_errors = []
    provincias = ['VI', 'AB', 'A', 'AL', 'AV', 'BA', 'PM', 'B', 'BU', 'CC', 'CA', 'CS', 'CR', 'CO', 'C', 'CU', 'GI', 'GR', 'GU', 'SS', 'H', 'HU', 'J', 'LE', 
        'L', 'LO', 'LU', 'M', 'MA', 'MU', 'NA', 'OR', 'O', 'P', 'GC', 'PO', 'SA', 'TF', 'S', 'SG', 'SE', 'SO', 'T', 'TE', 'TO', 'V', 'VA', 'BI', 'ZA', 'Z', 'CE', 'ML']
    count_provincias = dict((prov, 0) for prov in provincias)
    
    row_line = 2
    for row in reader:
        name = dict(row).__getitem__('name')
        _type = dict(row).__getitem__('type')
        born_area = dict(row).__getitem__('born_area')
        current_area = dict(row).__getitem__('current_area')
        primaries = dict(row).__getitem__('primaries')
        sex = dict(row).__getitem__('sex')
        candidatesGroupName = dict(row).__getitem__('candidatesGroup')
        
        if primaries == 'FALSE':
            primaries = False
            validation_errors.append("Error en la línea " + str(row_line) + ": El candidato " + str(name) + " no ha pasado el proceso de primarias")
        else:
            primaries = True

        try:
            candidatesGroup_Search = CandidatesGroup.objects.get(name=candidatesGroupName)
        except:
            candidatesGroup_Search = CandidatesGroup(name=candidatesGroupName).save()

        if _type == 'CANDIDATO':
            if born_area in count_provincias:
                count_provincias[born_area] = count_provincias[born_area] + 1

            if current_area in count_provincias:
                count_provincias[current_area] = count_provincias[current_area] + 1


        try:
            candidato = Candidate(name=name, type=_type, born_area=born_area, current_area=current_area, primaries= primaries, sex=sex, candidatesGroup=CandidatesGroup.objects.get(name=candidatesGroupName))
            candidato.full_clean()
        except ValidationError:
            validation_errors.append("Error en la línea " + str(row_line) + ": Hay errores de formato/validación")
        else:
            candidato.save()
        
        row_line = row_line + 1

    
    provincias_validacion = [prov for prov in provincias if count_provincias[prov] < 2]

    for prov in provincias_validacion:
        validation_errors.append("Tiene que haber al menos dos candidatos al congreso cuya provincia de nacimiento o de residencia tenga de código " + prov) 


    if len(validation_errors) > 0:
        transaction.set_rollback(True)
    
    return validation_errors



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
            self.serializer_class = SimpleVotingSerializer

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        for data in ['name', 'desc', 'question', 'question_opt']:
            if not data in request.data:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        question = Question(desc=request.data.get('question'))
        question.save()
        for idx, q_opt in enumerate(request.data.get('question_opt')):
            opt = QuestionOption(question=question, option=q_opt, number=idx)
            opt.save()
        voting = Voting(name=request.data.get('name'), desc=request.data.get('desc'),
                question=question)
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
