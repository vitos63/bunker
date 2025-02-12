from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from bunker_app.models import MemberCharact
from django.contrib.sessions.models import Session


@shared_task
def delete_old_data():
    threshold_time = timezone.now() - timedelta(minutes=30)
    MemberCharact.objects.filter(time_create__lt=threshold_time).delete()

@shared_task
def clear_old_sessions():
    now = timezone.now()
    expired_sessions = Session.objects.filter(expire_date__lt=now)
    expired_sessions.delete()

