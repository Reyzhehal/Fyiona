import smtplib
from typing import Optional
from email.mime.text import MIMEText

from django.conf import settings
from .models import CustomUser



def send_token_to_email(user: CustomUser, subject: str, body: Optional[str] = None, *args, **kwargs):
    msg = MIMEText(body,_charset="UTF-8")

    server = smtplib.SMTP("smtp.gmail.com")
    server.starttls()
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    msg["Subject"] = subject
    msg["From"] = settings.DEFAULT_FROM_EMAIL

    if kwargs.get("email"):
        to_email = kwargs.get("email")
    elif not user.is_anonymous:
        to_email = user.email
    else:
        raise ValueError(f"There is wrong Email address to send token!")
 
    msg["To"] = to_email
    server.sendmail(msg.get("From"), msg["To"], msg.as_string())

    return server.quit()