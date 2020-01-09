from django.urls import path
from . import views


urlpatterns = [
    path('', views.VotingView.as_view(), name='voting'),
    path('<int:voting_id>/', views.VotingUpdate.as_view(), name='voting'),
    path('load/', views.candidates_load, name='voting'),
    path('show/<int:voting>/', views.findVotingByParam, name='voting'),
    path('show/<str:voting>/', views.findVotingByParam, name='voting'),
    path('validate/', views.handle_uploaded_file, name='voting'),
    path('votings/', views.voting_list, name='votings'),
    path('votings/update/', views.voting_list_update, name='voting_update'),
    path('votings/update_selection/', views.voting_list_update_multiple, name='voting_update_multiple'),
    path('edit/', views.voting_edit, name='voting'),
    path('view', views.getVoting, name='voting_view'),
    path('create_auth/', views.create_auth, name="votings")
]
