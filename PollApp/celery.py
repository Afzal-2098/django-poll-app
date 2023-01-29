# from __future__ import absolute_import, unicode_literals
# import os

# from celery import Celery
# from django.conf import settings

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PollApp.settings")

# app = Celery("PollApp")
# app.conf.enable_utc = False

# app.conf.update(timezone = "Asia/Kolkata")

# app.config_from_objects(settings, namespace='celery')


# # celery Beat Settings

# app.autodiscover_tasks()

# @app.task(bind=True)
# def debug_task(self):
#     print(f"request: {self.request!r}")