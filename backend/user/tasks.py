import logging
from celery.exceptions import SoftTimeLimitExceeded

from common.communication import EmailSender
from common.decorators import count_queries
from config.celery import app

logger = logging.getLogger(__name__)


@app.task(time_limit=60)
@count_queries
def send_welcome_email(user_email):
    try:
        email = EmailSender()
        template = "users/welcome_email.html"
        context = {
            "name": user_email,
        }
        email.send(user_email, "Welcome to our platform", template, context)
    except SoftTimeLimitExceeded:
        logger.error(f"Time limit exceeded for {send_welcome_email.__name__} task")
