from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.listaCensos, name='listaCensos'),
    path('<int:voting_id>/', views.listaVotantes, name='listaVotantes'),
]
