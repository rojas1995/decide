from django.urls import path
from .views import BoothView, GetVoting


urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view()),
    path('getvoting/', GetVoting.as_view())
]
