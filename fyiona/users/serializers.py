import datetime as dt

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    Serializer,
    ValidationError,
    UUIDField,
    FileField
)

from .signals import change_email_signal
from .models import (
    UserProfile,
    CustomUser,
    CustomUserEmailConfirmationToken,
    AccessTokenToUpdateCustomUserFields
)

####################################################################################################
####################################################################################################
########################################## UserProfile #############################################
####################################################################################################
####################################################################################################


class UserProfileSerializer(ModelSerializer):
    """Serializer for list all UserProfiles from DB"""

    class Meta:
        model = UserProfile
        fields = (
            "avatar",
            "biography",
            "business_account",
        )


####################################################################################################
####################################### CustomUser #################################################
####################################################################################################

class CustomUserDetailSerializer(ModelSerializer):
    user_profile = UserProfileSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "user_profile",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "token_balance",
            "date_joined",
        )
        read_only_fields = ("id",)


class CustomUserListSerializer(ModelSerializer):
    user_profile = UserProfileSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = (
            "user_profile",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "token_balance"
        )



class CustomUserCreateSerializer(ModelSerializer):
    """
    Serializer made of UserProfile model and responsible for UserProfile creation.
    """

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


    class Meta:
        model = CustomUser
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "phone_number",
            "token",
        )
        read_only_fields = ("id", "token")



class CustomUserUpdateSerializer(ModelSerializer):
    """
    Serializer for list all users from DB UserProfile.
    Serializer for update CustomUser model.
    """

    first_name = CharField(max_length=32, required=False)
    last_name = CharField(max_length=32, required=False)
    avatar = FileField(required=False)
    biography = CharField(required=False)
    

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            "first_name",
            instance.first_name,
        )
        instance.last_name = validated_data.get(
            "last_name",
            instance.last_name,
        )
        instance.user_profile.avatar = validated_data.get(
            "avatar", instance.user_profile.avatar
        )
        instance.user_profile.biography = validated_data.get(
            "biography", instance.user_profile.biography
        )
        instance.save()

        return instance


    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "avatar",
            "biography"
        )


class CustomUserResetPasswordSerializer(ModelSerializer):
    id = UUIDField()
    password = CharField(min_length=8, write_only=True)


    def update(self, instance, validated_data):
        """
            Make sure this method return instance and nothing except that!
        """
        token = AccessTokenToUpdateCustomUserFields.objects.filter(user=instance).first()

        if not token:
            raise ValidationError(
                detail={
                    "success": False,
                    "result": f"Access token for {instance.email} does not exist!",
                }
            )


        token_created = dt.datetime.now().minute - token.date.minute
        
        if token_created > 10:
            token.delete()
            raise ValidationError(
                detail={
                    "success": False,
                    "result": f"Access token for {instance.email} has expired!",
                }
            )
        password = validated_data.get("password")
        instance.set_password(password)
        instance.save()
        token.delete()

        return instance


    class Meta:
        model = CustomUser
        fields = (
            "id",
            "password"
        )
        read_only_fields = ("id",)
        extra_kwargs = {'password': {'write_only': True}}


class CustomUserChangePasswordSerializer(ModelSerializer):
    old_password = CharField(write_only=True)
    new_password = CharField(write_only=True)


    def update(self, instance, validated_data):
        old_passowrd = validated_data.get("old_password")
        new_password = validated_data.get("new_password")


        if instance.check_password(new_password):
            raise ValidationError(
                detail={
                    "success": False,
                    "result": "New password is the same as the OLD password"
                }
            )

        if not instance.check_password(old_passowrd):
            raise ValidationError(
                detail={
                    "success": False,
                    "result": "The old password does not match"
                }
            )

        if instance.check_password(old_passowrd):
            instance.set_password(new_password)
            instance.save()

            return instance

        

    class Meta:
        model = CustomUser
        fields = (
            "old_password",
            "new_password"
        )
        extra_kwargs = {
            'old_passowrd': {'write_only': True},
            'new_password': {'write_only': True}
        }
####################################################################################################
####################################################################################################
######################################### Authentication ###########################################
####################################################################################################
####################################################################################################


class LoginSerializer(Serializer):
    """
        Serializer for authorization user. The user can log in using email or phone number. 
        First, there is a check by email, 
        if the email is empty, 
        then the serializer tries to authorize the user by phone number.
    """
    email = CharField(max_length=50, required=False)
    phone_number = CharField(max_length=20, required=False)
    password = CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=True,
        max_length=128,
        write_only=True,
    )

    def validate(self, data):
        username = data.get("email", data.get("phone_number", None))
        password = data.get("password")
        if not username:
            username = UserProfile.objects.get(
                phone_number=data.get('phone_number', None)).email

        if username and password:
            user = authenticate(
                username=username,
                password=password,
            )
            if not user:
                msg = "Wrong username or password..."
                raise ValidationError(
                    {
                        "success": False,
                        "result": str(msg),
                    }
                )

        else:
            msg = 'Must include "email/phone_number" and "password"...'
            raise ValidationError(
                {
                    "success": False,
                    "result": msg,
                }
            )

        return {
            "success": True,
            "result": {
                "email": user,
                "token": user.token,
            },
        }


class LoginAfterRegistrationSerializer(Serializer):
    """
    Serializer for user authorization immediately after registration.
    """
    token = CharField(max_length=200, write_only=True)

    def validate(self, data):
        username = data.get("email", data.get("phone_number"))
        password = data.get("password")

        if username and password:
            user = authenticate(
                username=username,
                password=password,
            )
            if not user:
                msg = "Wrong username or password..."
                raise ValidationError(
                    {
                        "success": "False",
                        "result": str(msg),
                    }
                )

        else:
            msg = 'Must include "email/phone_number" and "password"...'
            raise ValidationError(
                {
                    "success": False,
                    "result": msg,
                }
            )

        return {
            "success": True,
            "result": {
                "user": user,
                "token": user.token,
            },
        }



class EmailConfirmationSerializer(Serializer):
    """
        Serializer for code verification.
        This is a serializer for modifying account data. 
        User can change 5 fields: first_name, last_name, phone_number, user_biography, email.
        If the user wants to change the email, a confirmation link will be sent to the specified email.
    """

    def validate(self, attrs):
        user = UserProfile.objects.get(
            email=self.context.get('request').user.email)
        return self.update(instance=user, validated_data=attrs)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number.__str__())
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.user_biography = validated_data.get('user_biography', instance.user_biography)
        instance.save()

        if validated_data.get('email', None):
            change_email_signal.send(
                sender=self.__class__, 
                data=validated_data,
                instance=instance, 
                email=validated_data.get('email')
            )
        return instance

    class Meta:
        model = CustomUserEmailConfirmationToken

    confirmation_code = CharField(max_length=5, write_only=True)

    def confirmate(self, data):
        code = data.get("confirmation_code", None)

        if code is None:
            raise ValidationError("Confirmation code field is empty.")

        db_code = CustomUserEmailConfirmationToken.objects.get(user=data.user.username)
        db_code = code.get("code", "000000")

        if code != db_code:
            raise ValidationError("Invalid code.")