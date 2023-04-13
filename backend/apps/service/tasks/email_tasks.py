from smtplib import SMTPAuthenticationError

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import send_mail

from db.todo.models import Todo

logger = get_task_logger(__name__)


@shared_task(ignore_result=True, name='send_email')
def send_email(todo_id):
    todo = Todo.objects.filter(id=todo_id).first()
    if not todo:
        logger.error(f'Todo with id {todo_id} does not exist.')
        return
    try:
        send_mail(
            subject=todo.title,
            message=todo.description,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email for user in todo.assigned.all()],
        )
    except SMTPAuthenticationError:
        logger.error('Email authentication failed.')
