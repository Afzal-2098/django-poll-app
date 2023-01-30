from celery import shared_task
from App.models import Question
from datetime import datetime, timedelta

@shared_task(bind=True)
def DeletePoll(self):
    # operations
    time_threshold = datetime.now() - timedelta(hours=24)
    results = Question.objects.filter(pub_date__lt = time_threshold)
    print(results)
    # results.delete()
    return "Polls older than 12 hours, deleted!"