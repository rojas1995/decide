from django.urls import path
from .views import GetVoting, PageView, votinglist, booth
from django.conf.urls import url,include

urlpatterns = [
    path('login/', PageView.login),
    path('', PageView.index),
    path('logout/', PageView.logout),
    path('register/', PageView.register),
    path('<int:voting_id>/', booth),
    path('list/', votinglist),
    path('profile/', PageView.profile),
    path('getvoting/', GetVoting.as_view()),
    url(r'^i18n/', include('django.conf.urls.i18n'))
]
