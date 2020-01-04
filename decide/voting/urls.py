from django.urls import path
from . import views


urlpatterns = [
    path('', views.VotingView.as_view(), name='voting'),
    path('<int:voting_id>/', views.VotingUpdate.as_view(), name='voting'),
    path('load/', views.candidates_load, name='voting'),
    path('votings/', views.voting_list, name='votings'),
    path('votings/delete/', views.voting_list_delete, name='voting_delete'),
    path('votings/start/', views.voting_list_start, name='voting_start'),
    path('votings/stop/', views.voting_list_stop, name='voting_stop'),
    path('votings/tally/', views.voting_list_tally, name='voting_tally'),
]
