import os
import sys
import inspect

import django
from django.db.utils import IntegrityError
import pytest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fyiona.settings")
django.setup()

from users import models as users_models
from posts import models as posts_models
from umessages import models as umessages_models


@pytest.fixture(scope="module")
def custom_user_object():
    user = users_models.CustomUser(
        email="azatot@gmail.com",
        first_name="Azatot",
        last_name="Nirlatotep",
        phone_number="+996550271098",
    )
    user.set_password("Ykt4tVFd8bbk")
    return user


@pytest.mark.django_db
class TestCustomUser:
    def test_custom_user_creation(self, custom_user_object: users_models.CustomUser):
        custom_user_object.save()
        try:
            user_in_db = users_models.CustomUser.objects.get(email="azatot@gmail.com")
        except users_models.CustomUser.DoesNotExist:
            created = False
        else:
            created = True

        assert created
        assert user_in_db.password != ""

    def test_user_exists_with_email(self, custom_user_object: users_models.CustomUser):
        custom_user_object.save()
        with pytest.raises(IntegrityError):
            user = users_models.CustomUser.objects.create(
                email="azatot@gmail.com",
                first_name="Azatot",
                last_name="Nirlatotep",
                phone_number="+996550271098",
            )
            user.set_password("Ykt4tVFd8bbk")

            assert user.password != ""

    def test_user_exists_with_phone_number(
        self, custom_user_object: users_models.CustomUser
    ):
        custom_user_object.save()
        with pytest.raises(IntegrityError):
            user: users_models.CustomUser = users_models.CustomUser.objects.create(
                email="test@gmail.com",
                first_name="Azatot",
                last_name="Nirlatotep",
                phone_number="+996550271098",
            )
            user.set_password("Ykt4tVFd8bbk")

            assert user.password != ""

    def test_created_user_default_values(
        self, custom_user_object: users_models.CustomUser
    ):
        custom_user_object.save()

        user_in_db: users_models.CustomUser = users_models.CustomUser.objects.get(
            email="azatot@gmail.com"
        )
        assert user_in_db.password != ""
        assert user_in_db.token_balance == 0
        assert user_in_db.phone_number_confirmed == False
        assert user_in_db.user_profile
        assert user_in_db.user_profile.business_account == False
