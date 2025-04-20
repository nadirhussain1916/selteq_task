import logging
from celery import shared_task
from .models import Task

logger = logging.getLogger(__name__)

@shared_task
def print_user_tasks(user_id):
    """Logs tasks of user with ID 1 with specific fields as required."""
    tasks = Task.objects.filter(user_id=user_id).order_by('-created_at')

    if not tasks:
        logger.info(f"No tasks found for user with ID {user_id}.")
        return

    for task in tasks:
        logger.info(
            f"Task Title: {task.title}\n"
            f"Duration: {task.duration} minutes\n"
            f"Created at: {task.created_at}\n"
            f"Updated at: {task.updated_at}\n"
            f"------------------------"
        )