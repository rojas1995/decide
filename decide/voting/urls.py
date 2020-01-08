from django.urls import path
from . import views


urlpatterns = [
    path('', views.VotingView.as_view(), name='voting'),
    path('<int:voting_id>/', views.VotingUpdate.as_view(), name='voting'),
    path('load/', views.candidates_load, name='voting'),
    path('votings/', views.voting_list, name='votings'),
    path('votings/update/', views.voting_list_update, name='voting_update'),
    path('votings/update_selection/', views.voting_list_update_multiple, name='voting_update_multiple'),
]
