from django.urls import path
from .views import BoothView, GetVoting


urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view()),
    path('login/', BoothView.login),
    path('', BoothView.llamarIndex),
    path('logout/', BoothView.logout),
    path('register/', BoothView.register),
    path('getvoting/', GetVoting.as_view())
]
