from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Custom UserManager class allows to control user creation process."""

    def create_user(self, email, password=None, **extra_fields):
        """The main function is responsible for EVERY user creation."""
        if not email:
            raise ValueError(
                "User MUST have an Email, please provide an Email!")

        staff_email = self.normalize_email(email)
        user = self.model(email=staff_email, **extra_fields)
        user.is_banned = False
        user.active = False

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """This function is responsibleonly if you want to create a user who has an access to Admin page."""
        user = self.create_user(email, password=password)
        user.staff = True
        user.active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """This function is responsibleonly if you want to create a superuser"""
        user = self.create_user(email, password=password, **extra_fields)
        user.staff = True
        user.admin = True
        user.active = True
        user.position = "admin"
        user.save(using=self._db)
        return 1
