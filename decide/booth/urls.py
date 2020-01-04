from django.urls import path
from .views import GetVoting, PageView, votinglist, booth


urlpatterns = [
    path('<int:voting_id>/', booth),
    path('', PageView.index),
    path('list/', votinglist),
    path('getvoting/', GetVoting.as_view())
]
