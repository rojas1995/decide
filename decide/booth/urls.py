from django.urls import path
from .views import BoothView, GetVoting, PageView, votinglist


urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view()),
    path('', PageView.index),
    path('list/', votinglist),
    path('getvoting/', GetVoting.as_view())
]
