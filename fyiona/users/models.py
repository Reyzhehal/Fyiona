import uuid
import secrets
from datetime import datetime, timedelta

import jwt
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from . import managers


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("User ID"),
    )

    email = models.EmailField(
        unique=True,
        max_length=64,
        db_index=True,
        verbose_name=_("Email Address"),
    )

    first_name = models.CharField(
        max_length=32,
        db_index=True,
        verbose_name=_("First Name"),
    )

    last_name = models.CharField(
        max_length=32,
        db_index=True,
        verbose_name=_("Last Name"),
    )

    phone_number = PhoneNumberField(
        db_index=True,
        # unique=True, TODO: [FYION-34] If the phone_number is unique then there are cannot be 2 users with empty phone numbers, otherwise, 2 users can have the same phone number
        blank=True,
        verbose_name=_("Phone Number"),
    )

    phone_number_confirmed = models.BooleanField(
        default=False,
        verbose_name=_("Phone Number confirmed"),
    )

    email_confirmed = models.BooleanField(
        default=False,
        verbose_name=_("Email confirmed"),
    )
 
    token_balance = models.BigIntegerField(
        default=0,
        verbose_name=_("Balance"),
    )

    date_joined = models.DateField(verbose_name=_("Date Joined"), default=timezone.now)
    active = models.BooleanField(verbose_name=_("Is_Active"), default=True)
    staff = models.BooleanField(verbose_name=_("Is_Staff"), default=False)
    admin = models.BooleanField(verbose_name=_("Is_Admin"), default=False)

    objects = managers.UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = (
        "first_name",
        "last_name",
        "phone_number",
    )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def token(self):
        """This property field allows to get user's current token"""
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        This private method is responsible for generating unique JWT every time this method called.
        """
        dt = datetime.now() + timedelta(minutes=settings.TOKEN_LIFETIME)
        token = jwt.encode(
            {"id": f"{self.pk}", "exp": dt.utcfromtimestamp(dt.timestamp())},
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    """
    This model depends on model CustomUser and has 5 fields:
    user --> CustomUser relation
    avatar --> Avatar picture of user
    biography --> Description of the user, which he writes himself
    business_account --> Logical field. If True, this is a user with a business account; otherwise, it is not.
    followers --> Relations with followers of user
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.PROTECT,
        related_name="user_profile",
    )

    avatar = models.ImageField(
        verbose_name=_("User Profile Photo"),
        upload_to="accounts/profiles/",
        default="default_profile_image.png",
    )

    biography = models.TextField(
        verbose_name=_("Short Buography about User"),
        default="I am cool person!",
    )

    business_account = models.BooleanField(
        verbose_name=_("Is Premium User"),
        default=False,
    )

    followers = models.ManyToManyField('self', symmetrical=False, blank=True)


    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


class CustomUserEmailConfirmationToken(models.Model):
    """
    This model has 2 fields:
    user --> user email
    token --> the confirmation token that was sent to the email
    """

    # def __init__(self, *args, **kwargs):
    #     super(EmailConfirmationToken, self).__init__(*args, **kwargs)

    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name="confirmation_token",
    )

    token = models.CharField(
        verbose_name=_("Confirmation Token"),
        max_length=128,
        default=secrets.token_hex(64)
    )

    class Meta:
        verbose_name = "Account Confirmation Token"
        verbose_name_plural = "Account Confirmation Tokens"

    def __str__(self):
        return self.token


class AccessTokenToUpdateCustomUserFields(models.Model):
    user = models.OneToOneField(
        to=CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_("Client Email"),
    )

    token = models.CharField(
        max_length=128,
        default=secrets.token_hex(64),
        verbose_name=_("Client Password Reset Token"),
    )

    date = models.DateTimeField(
        verbose_name=_("Password Reset Token Lifetime"),
        auto_now=True,
        db_index=True,
    )

    class Meta:
        verbose_name = "Reset Password Token"
        verbose_name_plural = "Reset Password Tokens"

    def __str__(self):
        return self.token


class AccessTokenToDeleteCustomUser(models.Model):
    user = models.OneToOneField(
        to=CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_("Account Email"),
    )

    token = models.CharField(
        max_length=128,
        default=secrets.token_hex(64),
        verbose_name=_("Delete Account Access Token"),
    )

    date = models.DateTimeField(
        verbose_name=_("Date Created"),
        auto_now=True,
        db_index=True,
    )

    class Meta:
        verbose_name = "Reset Password Token"
        verbose_name_plural = "Reset Password Tokens"

    def __str__(self):
        return self.token