from datetime import datetime
import os
from apscheduler.schedulers.background import BackgroundScheduler

from django.utils import timezone

def start_votings():
    from voting.models import Voting
    now = timezone.now()
    print(now.date())
    print(now.time())
    
    findAllByNowDateSelected = Voting.objects.filter(start_date_selected__lte = now, pub_key=None)
    
    if findAllByNowDateSelected.count() > 0:
        for v in findAllByNowDateSelected:
            v.start_date = now
            Voting.create_pubkey(v)

def end_votings():
    from voting.models import Voting
    now = timezone.now()
    findAllByNowDateSelected = Voting.objects.filter(end_date_selected__lte=now)
    
    if findAllByNowDateSelected.count() > 0:
        for v in findAllByNowDateSelected:
            v.end_date = now
            v.save()

# Invocamos el planificador
def start():
    # Creamos un objeto planificador
    scheduler = BackgroundScheduler()

    #Añadimos la tarea definiendo una funcion para que se ejecute en el intervalor que le marquemos.
    # Consultar: https://apscheduler.readthedocs.io/en/latest/userguide.html
    scheduler.add_job(start_votings, 'interval', minutes=30)
    scheduler.add_job(end_votings, 'interval', minutes=30)
    # Le damos instrucciones al planificador para que comience
    scheduler.start()
    