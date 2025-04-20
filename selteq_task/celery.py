import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'selteq_task.settings')

app = Celery('selteq_task')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'print-user1-tasks-every-minute': {
        'task': 'tasks.tasks.print_user_tasks',
        'schedule': 60.0,
        'args': (1,),
    },
}

@app.task(bind=True)
def debug_task(self):
    """Debug task to print the request."""
    print(f'Request: {self.request!r}')