from django.urls import path
from .views import GetVoting, PageView, votinglist, booth


urlpatterns = [
    path('login/', PageView.login),
    path('', PageView.index),
    path('logout/', PageView.logout),
    path('register/', PageView.register),
    path('<int:voting_id>/', booth),
    path('list/', votinglist),
    path('profile/', PageView.profile),
    path('getvoting/', GetVoting.as_view())
]
