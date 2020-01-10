from rest_framework import serializers

from .models import Voting, Candidate, CandidatesGroup
from base.serializers import KeySerializer, AuthSerializer

class CandidateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Candidate
        fields = ('id', 'name', 'type','born_area', 'current_area', 'primaries', 'sex')

class CandidateGroupSerializer(serializers.HyperlinkedModelSerializer):
    candidates = CandidateSerializer(many=True)
    class Meta:
        model = CandidatesGroup
        fields = ('id', 'name', 'candidates')

#class QuestionOptionSerializer(serializers.HyperlinkedModelSerializer):
 #   class Meta:
 #       model = QuestionOption
  #      fields = ('number', 'option')


#class QuestionSerializer(serializers.HyperlinkedModelSerializer):
#    options = QuestionOptionSerializer(many=True)
#    class Meta:
#        model = Question
#        fields = ('desc', 'options')


class VotingSerializer(serializers.HyperlinkedModelSerializer):
    #question = QuestionSerializer(many=False)
    candidatures = CandidateGroupSerializer(many=True) 
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)

    class Meta:
        model = Voting
        fields = ('id', 'name', 'desc', 'candidatures', 'start_date',
                  'end_date', 'pub_key', 'auths', 'tally', 'postproc')


class SimpleVotingSerializer(serializers.HyperlinkedModelSerializer):
 #   question = QuestionSerializer(many=False)

    class Meta:
        model = Voting
        fields = ('name', 'desc', 'start_date', 'end_date')
