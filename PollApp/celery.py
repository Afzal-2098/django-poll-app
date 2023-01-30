from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PollApp.settings")

app = Celery("PollApp")
app.conf.enable_utc = False

app.conf.update(timezone = "Asia/Kolkata")

app.config_from_object(settings, namespace='CELERY')


# celery Beat Settings
app.conf.beat_schedule = {
    "delete_poll_at_12": {
        'task': 'App.tasks.DeletePoll',
        'schedule': crontab(minute="*/1"),   # hour = "*/24"
        # 'args':
    }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"request: {self.request!r}")