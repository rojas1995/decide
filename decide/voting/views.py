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

def handle_uploaded_file(f):
    reader = csv.DictReader(codecs.iterdecode(f, 'utf-8'), delimiter="#")
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
            candidatesGroup_Search = CandidatesGroup.objects.get(name=candidatesGroupName)
        except:
            candidatesGroup_Search = CandidatesGroup(name=candidatesGroupName).save()
        
        Candidate(name=name, type=_type, born_area=born_area, current_area=current_area, primaries= primaries, sex=sex, candidatesGroup=CandidatesGroup.objects.get(name=candidatesGroupName)).save()

def voting_list(request):
    votings = Voting.objects.all()
    return render(request, "votings.html", {'votings':votings, 'STATIC_URL':settings.STATIC_URL})

def voting_list_start(request):
    voting_id = request.POST['voting_id']
    voting = get_object_or_404(Voting, pk=voting_id)
    action = request.POST['action']
    if action == 'start':
        if voting.start_date:
            msg = "None"
        else:
            voting.start_date = timezone.now()
            voting.save()

    return HttpResponseRedirect('/voting/votings/')

def voting_list_stop(request):
    voting_id = request.POST['voting_id']
    voting = get_object_or_404(Voting, pk=voting_id)
    action = request.POST['action']
    if action == 'start':
        if voting.start_date:
            msg = 'Voting already started'
            st = status.HTTP_400_BAD_REQUEST
        else:
            voting.start_date = timezone.now()
            voting.save()
            msg = 'Voting started'
            st = status.HTTP_200_OK

    return HttpResponseRedirect('/admin/')

def voting_list_tally(request):
    voting_id = request.POST['voting_id']
    voting = get_object_or_404(Voting, pk=voting_id)
    action = request.POST['action']
    if action == 'start':
        if voting.start_date:
            msg = 'Voting already started'
            st = status.HTTP_400_BAD_REQUEST
        else:
            voting.start_date = timezone.now()
            voting.save()
            msg = 'Voting started'
            st = status.HTTP_200_OK

    return HttpResponseRedirect('/admin/')

def voting_list_delete(request):
    voting_id = request.POST['voting_id']
    voting = get_object_or_404(Voting, pk=voting_id)
    action = request.POST['action']
    if action == 'start':
        if voting.start_date:
            msg = 'Voting already started'
            st = status.HTTP_400_BAD_REQUEST
        else:
            voting.start_date = timezone.now()
            voting.save()
            msg = 'Voting started'
            st = status.HTTP_200_OK

    return HttpResponseRedirect('/admin/')

def voting_list_update(request):
    array_voting_id = request.POST['array_voting_id[]'].split(",")
    for voting_id in array_voting_id:
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
