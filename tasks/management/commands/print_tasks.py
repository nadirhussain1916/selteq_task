import time
import logging
from django.core.management.base import BaseCommand
from tasks.models import Task

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """Prints all tasks one by one with a 10-second interval."""
    help = 'Prints all tasks one by one with a 10-second interval'

    def handle(self, *args, **kwargs):
        tasks = Task.objects.all()

        if not tasks.exists():
            logger.warning("No tasks found in the database.")
            return

        for task in tasks:
            task_info = (
                f"Task ID: {task.id}, Title: {task.title}, Duration: {task.duration}, "
                f"Created by: {task.user.username}, Created at: {task.created_at}"
            )
            logger.info(task_info)
            time.sleep(10)