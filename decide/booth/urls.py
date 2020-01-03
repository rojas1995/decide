from django.urls import path
from .views import GetVoting, PageView, votinglist, VotingProcess


urlpatterns = [
    path('<int:voting_id>/', VotingProcess.booth),
    path('', PageView.index),
    path('list/', votinglist),
    path('getvoting/', GetVoting.as_view())
]
