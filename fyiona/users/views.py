import random
import string
import datetime

from django.db.models import Q
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, views
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly

from .signals import login_signal

from .utilities import send_token_to_email
from .middlewares import JWTAuthentication

from .serializers import (
    CustomUserDetailSerializer,
    CustomUserListSerializer,
    CustomUserCreateSerializer,
    CustomUserUpdateSerializer,
    CustomUserResetPasswordSerializer,
    CustomUserChangePasswordSerializer,

    LoginSerializer,
    CustomUserEmailConfirmationToken,
)


from .models import (
    CustomUser,
    UserProfile,
    AccessTokenToDeleteCustomUser,
    CustomUserEmailConfirmationToken,
    AccessTokenToUpdateCustomUserFields,
    UserProfile,
)

####################################################################################################
###################################### CUSTOM USER CRUD ############################################
####################################################################################################

class CustomUserCreateAPIView(generics.CreateAPIView):
    """
    This View is only responsible for creation of TWO models: CustomUser and UserProfile
    We create CustomUser through UserProfile model.
    When client fill out the form he provides the data for two models at once.
    """

    permission_classes = (AllowAny,)
    serializer_class = CustomUserCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # user = authenticate(
        #     username=request.data.get("email", None),
        #     password=request.data.get("password", None),
        # )

        # login_signal.send(sender=self.__class__, data=request.data, key=user.token)
        return Response(
            data={
                "success": True,
                "result": "Please confirm your email to Log In",
            },
            status=status.HTTP_200_OK,
        )



class CustomUserPatchAPIView(generics.UpdateAPIView):
    """
    Serializer for update user.
    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = CustomUserUpdateSerializer

    def patch(self, request, *args, **kwargs):
        if not request.data or '' in request.data.keys():
            return Response(
                data={
                    "success": False,
                    "result": "Please provide at least on field to update",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        for key in request.data.keys():
            if key not in ("first_name", "last_name", "avatar", "biography"):
                return Response(
                    data={
                        "success": False,
                        "result": f"Wrong field - {key}",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = self.serializer_class(
            instance=request.user,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()


        return Response(
            data={
                "success": True,
                "result": "Data has been changed successfully",
            },
            status=status.HTTP_200_OK,
        )



class CustomUserDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = CustomUserDetailSerializer

    def get(self, request):
        token = request.GET.get("token")
        user_in_db = AccessTokenToDeleteCustomUser.objects.filter(token=token).first()

        if user_in_db:
            user_in_db.user.user_profile.delete()
            user_in_db.user.delete()
            user_in_db.delete()

        return Response(
            data={
                "success": True,
                "result": f"User {user_in_db.user.email} has been deleted successfully"
            },
            status=status.HTTP_200_OK
        )


    def delete(self, request):
        token_in_db = AccessTokenToDeleteCustomUser.objects.filter(user=request.user).first()

        if token_in_db:
            token = token_in_db
        else:
            token = AccessTokenToDeleteCustomUser.objects.create(user=request.user)

        token_url = f"{settings.DOMAIN_NAME}/api/v1/accounts/delete?token={token}"

        body = f"""Dear {request.user.first_name} {request.user.last_name},

IMPORTANT:
You just have sent a request to delete Your account!
As soon as you follow the link below, your account will be deleted, think twice!

Please, follow the link bellow to delete Your account:
{token_url}"""

        send_token_to_email(
            user=request.user,
            subject="Delete Account",
            body=body,
            email=request.user.email
        )

        return Response(
            data={
                "success": True,
                "result": f"We sent confirmation link to {request.user.email} to remove this account"
            },
            status=status.HTTP_200_OK
        )



class CustomUserListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = CustomUserListSerializer

    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        serializer = self.serializer_class(users, many=True)

        return Response(
            data={
                "success": True,
                "result": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


    
class CustomUserDetailAPIView(generics.RetrieveAPIView):
    """
    View for detailed viewing of post.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = CustomUserDetailSerializer

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=request.user.pk)
        serializer = self.serializer_class(instance=user)
        
        return Response(
            data={
                "success": True, 
                "result": serializer.data
            }, 
            status=status.HTTP_200_OK
        )



class CustomUserSearchByEmailAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = CustomUserListSerializer

    queryset = CustomUser.objects.all()

    def get(self, request, *args, **kwargs):
        email = request.GET.get("email")
        if email:
            found = self.queryset.filter(Q(email__icontains=email) | Q(email__search=email))
            serializer = self.serializer_class(found, many=True)

            return Response(
                data={
                    "success": True,
                    "result": serializer.data
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            data={
                "success": False,
                "result": "The \"email\" query parameter was not provided!"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )



class CustomUserSearchByPhoneNumberAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = CustomUserListSerializer

    queryset = CustomUser.objects.all()

    def get(self, request, *args, **kwargs):
        phone_number = request.GET.get("phone_number")
        if phone_number:
            found = self.queryset.filter(
                Q(phone_number__icontains=phone_number) | Q(phone_number__search=phone_number)
            )
            serializer = self.serializer_class(found, many=True)

            return Response(
                data={
                    "success": True,
                    "result": serializer.data
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            data={
                "success": False,
                "result": "The \"phone_number\" query parameter was not provided!"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

####################################################################################################
####################################################################################################
####################################################################################################



####################################################################################################
#################################### AUTHORIZATION VIEWS ###########################################
####################################################################################################

class LoginAPIView(APIView):
    """
    The logic of this class is not to authenticate a user from the beginning but update the login state instead.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get("result").get("email")
        if user.email_confirmed:
            serializer.validated_data.get("result").update({"email": user.email})

            update_last_login(None, user)
            return Response(
                data=serializer.validated_data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={
                    "success": False, 
                    "result": "Email is not confirmed"
                }, 
                status=status.HTTP_403_FORBIDDEN
            )



# class LoginAfterRegistrationAPIView(APIView):
#     permission_classes = (AllowAny,)
#     serializer_class = LoginSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(
#             {"success": True, "result": serializer.data}, status=status.HTTP_200_OK
#         )

####################################################################################################
####################################################################################################
####################################################################################################


####################################################################################################
################################## ACCOUNT RECOVERY VIEWS ##########################################
####################################################################################################

class SendRequestToResetCustomUserPasswordAPIView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        user_email = request.data.get("email")

        if user_email:
            user = CustomUser.objects.filter(email=user_email).first()

            if user:
                token_in_db = AccessTokenToUpdateCustomUserFields.objects.filter(user=user).first()
                if token_in_db:
                    token = token_in_db
                else:
                    token = AccessTokenToUpdateCustomUserFields.objects.create(user=user)

                token_url = f"{settings.DOMAIN_NAME}/api/v1/accounts/password/reset/confirmation?token={token}"

                body = f"""Dear {user.first_name} {user.last_name},

You just have sent a request to reset Your password!

Please, follow the link bellow to reset Your password:
{token_url}"""

                send_token_to_email(
                    user=user,
                    subject="Password Reset",
                    body=body,
                    email=user_email
                )
                return Response(
                    data={
                        "success": True,
                        "result": "The instructions to reset the password have been sent to Your email"
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                data={
                    "success": False,
                    "result": "There is no user with such Email address!"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            data={
                "success": False,
                "result": "\"email\" field is empty!"
            },
            status=status.HTTP_404_NOT_FOUND
        )
        


class CustomUserResetPasswordAPIView(views.APIView):
    """
    This class deals with password reset.
    """
    permission_classes = (AllowAny,)
    serializer_class = CustomUserResetPasswordSerializer

    def get(self, request, *args, **kwargs):
        """
        This function is concerned with checking the correctness of the data and setting a new password.
        """
        token = request.GET.get("token")
        user_in_db = AccessTokenToUpdateCustomUserFields.objects.filter(token=token).first()

        if user_in_db:
            user_data = CustomUserDetailSerializer(user_in_db.user)
            return Response(
                data={
                    "success": True,
                    "result": user_data.data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            data={
                "success": False,
                "result": "Reset token is invalid",
            },
            status=status.HTTP_404_NOT_FOUND,
        )
            

    def patch(self, request, *args, **kwargs):
        user = CustomUser.objects.filter(id=request.data.get("id")).first()

        if user:
            serializer = self.serializer_class(user, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data={
                    "success": True,
                    "result": "Password updated successfully",
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            data={
                "success": False,
                "result": "Invalid UUID, such user does not exist",
            },
            status=status.HTTP_404_NOT_FOUND,
        )

####################################################################################################
####################################################################################################
####################################################################################################

class CustomUserChangePasswordAPIView(generics.UpdateAPIView):
    """
    This class is engaged in resetting and setting a new password.
    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = CustomUserChangePasswordSerializer

    def patch(self, request, *args, **kwargs):
        """
        This function is designed to check the correctness of the data and set a new password. 
        The new password cannot be the same as the old one.
        """

        serializer = self.serializer_class(request.user, request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={
                "success": True,
                "result": "Password has been updated successfully",
            },
            status=status.HTTP_200_OK,
        )


class ChangeUserProfileAPIView(APIView):
    """
    Serializer for update user.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserDetailSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request},
        )
        
        if serializer.is_valid():
            return Response(
                data={
                    "success": True,
                    "result": "Data has been changed successfully",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data={
                    "success": False,
                    "result": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )



class FollowAPIView(APIView):
    """
    Serializer for following.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, uuid, *args, **kwargs):
        
        follow = CustomUser.objects.filter(id=uuid).first()
        if follow:
            follow.user_profile.followers.add(request.user.user_profile)
            follow.save()

            return Response(
                {
                    "success": True,
                    "result": "Success",
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "success": False,
                "result": "User with this UUID does not exist.",
            },
            status=status.HTTP_404_NOT_FOUND,
        )

####################################################################################################
###################################### CONFIRMATION VIEWS ##########################################
####################################################################################################

class CustomUserEmailConfirmationAPIViev(views.APIView):
    """
    When navigating to this API, a token is retrieved from the link. 
    Then, the record in the database that owns this token,
    the email_confirmed attribute is changed to True, and the EmailConfirmationToken entry is removed.
    """
    permission_classes = (AllowAny,)
    serializer_class = CustomUserEmailConfirmationToken

    def get(self, request, token):
        confirmation_token = CustomUserEmailConfirmationToken.objects.filter(token=token).first()
        if confirmation_token:
            confirmation_token.user.email_confirmed = True
            confirmation_token.user.active = True
            confirmation_token.user.save()
            confirmation_token.delete()
            return Response(
                data={
                    "success": True, 
                    "result": "You email is confirmed. Now you can log in."
                }, 
                status=status.HTTP_200_OK
            )
        return Response(
            data={
                "success": False, 
                "result": "Page does not exist"
            }, 
            status=status.HTTP_404_NOT_FOUND
        )



class CustomUserChangeEmailConfirmationAPIView(APIView):
    """
    View for change email.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserDetailSerializer
    authentication_classes = (JWTAuthentication,)

    def get(self, request, *args, **kwargs):
        delete_token = AccessTokenToUpdateCustomUserFields.objects.get(user=request.user.email)
        delete_token.delete()
        user = CustomUser.objects.get(pk=request.user.pk)
        user.email = request.get_full_path().split("~")[1]
        user.save()

        return Response(
            data={
                "success": True,
                "result": "Email has been changed successfully",
            },
            status=status.HTTP_200_OK,
        )

####################################################################################################
####################################################################################################
####################################################################################################