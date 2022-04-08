import string
import random
import smtplib
import datetime
from email.mime.text import MIMEText


from django.conf import settings
from django.dispatch import receiver, Signal
from django.db.models.signals import post_save
from django_rest_passwordreset.signals import reset_password_token_created

from .utilities import send_token_to_email
from .models import UserProfile, AccessTokenToUpdateCustomUserFields, CustomUser, CustomUserEmailConfirmationToken


login_signal = Signal()
change_email_signal = Signal()


####################################################################################################
###################################### CUSTOM USER CREATION ########################################
####################################################################################################
@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

        token = CustomUserEmailConfirmationToken.objects.create(user=instance)
        token_url = f"{settings.DOMAIN_NAME}/api/v1/accounts/registration/confirmation/{token}"
        message_text = f"Follow the link below to confirm your Email address:\n{token_url}"

        send_token_to_email(
            user=instance, 
            subject="Confirmation Email Token",
            body=message_text
        )


@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.user_profile.save()

####################################################################################################
####################################################################################################
####################################################################################################



####################################################################################################
####################################################################################################
####################################################################################################

@receiver(reset_password_token_created)
def password_reset_token_created(
    instance, reset_password_token, sender=UserProfile, *args, **kwargs
):
    """
    Signal for send token on email after password reset.
    First, it tries to retrieve the token from the database,
    if the token does not exist or its age is more than 1 hour,
    then it generates a new token.
    """
    
    user_password_reset_token = None
    try:
        user_password_reset_token = AccessTokenToUpdateCustomUserFields.objects.get(
            user=reset_password_token.user.email
        )
    except:
        pass
    characters = string.ascii_letters + string.digits
    if user_password_reset_token:
        age = datetime.datetime.now().replace(
            tzinfo=None
        ) - user_password_reset_token.date.replace(tzinfo=None)
        if bool(age.seconds // 3600):
            delete_password_reset_token = AccessTokenToUpdateCustomUserFields.objects.get(
                user=reset_password_token.user.email
            )
            delete_password_reset_token.delete()
            random_token = "".join(random.choice(characters) for i in range(120))
            save_password_reset_token = AccessTokenToUpdateCustomUserFields(
                user=reset_password_token.user.email, token=random_token
            )
            save_password_reset_token.save()

    else:
        random_token = "".join(random.choice(characters) for i in range(120))
        save_password_reset_token = AccessTokenToUpdateCustomUserFields(
            user=reset_password_token.user.email, token=random_token
        )
        save_password_reset_token.save()

    user_password_reset_token = None

    try:
        user_password_reset_token = AccessTokenToUpdateCustomUserFields.objects.get(
            user=reset_password_token.user.email
        )
    except:
        pass

    characters = string.ascii_letters + string.digits

    if user_password_reset_token:
        age = datetime.datetime.now().replace(
            tzinfo=None
        ) - user_password_reset_token.date.replace(tzinfo=None)

        if bool(age.seconds // 3600):
            delete_password_reset_token = AccessTokenToUpdateCustomUserFields.objects.get(
                user=reset_password_token.user.email
            )

            delete_password_reset_token.delete()
            random_token = "".join(random.choice(characters) for i in range(120))
            save_password_reset_token = AccessTokenToUpdateCustomUserFields(
                user=reset_password_token.user.email, token=random_token
            )
            save_password_reset_token.save()

    else:
        random_token = "".join(random.choice(characters) for i in range(120))
        save_password_reset_token = AccessTokenToUpdateCustomUserFields(
            user=reset_password_token.user.email, token=random_token
        )
        save_password_reset_token.save()

    email_plaintext_message = "%s/api/v1/accounts/password_reset/confirmation/%s" % (
        settings.DOMAIN_NAME,
        AccessTokenToUpdateCustomUserFields.objects.get(user=reset_password_token.user.email).token,
    )

    msg = MIMEText(
        "Please follow the link to reset your password.\nThis link is active for 1 hour only!\n\n%s"
        % email_plaintext_message,
        _charset="UTF-8",
    )
    server = smtplib.SMTP("smtp.gmail.com")
    server.starttls()
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    msg["Subject"] = "Reset Password Request"
    msg["From"] = settings.DEFAULT_FROM_EMAIL
    msg["To"] = reset_password_token.user.email
    server.sendmail(msg.get("From"), msg["To"], msg.as_string())
    server.quit()

####################################################################################################
####################################################################################################
####################################################################################################



####################################################################################################
####################################################################################################
####################################################################################################

@receiver(change_email_signal)
def send_email_for_change_email(data, instance, *args, **kwargs):
    """
    A signal to send an email with a URL to a new email if the user wants to change the email address.
    I have nothing more to add, but there should be 2 sentences, so I wrote this.
    """

    user_email_confirmation_token = None
    try:
        user_email_confirmation_token = AccessTokenToUpdateCustomUserFields.objects.get(user=instance.email)
    except:
        pass

    characters = string.ascii_letters + string.digits

    if user_email_confirmation_token:
        age = datetime.datetime.now().replace(
            tzinfo=None
        ) - user_email_confirmation_token.date.replace(tzinfo=None)

        if bool(age.seconds // 3600):
            delete_email_token = AccessTokenToUpdateCustomUserFields.objects.get(user=instance.email)
            delete_email_token.delete()
            random_token = (
                "".join(random.choice(characters) for i in range(120))
                + "~"
                + data.get("email")
            )

            save_email_confirmation_token = AccessTokenToUpdateCustomUserFields(
                user=instance.email, token=random_token
            )
            save_email_confirmation_token.save()
    else:
        random_token = (
            "".join(random.choice(characters) for i in range(120))
            + "~"
            + data.get("email")
        )
        save_email_confirmation_token = AccessTokenToUpdateCustomUserFields(
            user=instance.email, token=random_token
        )
        save_email_confirmation_token.save()

    email_plaintext_message = "%s/api/v1/users/email_reset/confirmation/%s" % (
        settings.DOMAIN_NAME,
        AccessTokenToUpdateCustomUserFields.objects.get(user=instance.email).token,
    )

    msg = MIMEText(
        "Please follow the link to reset your email.\nThis link is active for 1 hour only!\n\n%s"
        % email_plaintext_message,
        _charset="UTF-8",
    )
    server = smtplib.SMTP("smtp.gmail.com")
    server.starttls()
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    msg["Subject"] = "Confirmation New Email"
    msg["From"] = settings.DEFAULT_FROM_EMAIL
    msg["To"] = data.get("email")
    server.sendmail(msg.get("From"), msg["To"], msg.as_string())
    server.quit()

####################################################################################################
####################################################################################################
####################################################################################################