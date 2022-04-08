from django.urls import path, re_path, include
from users import views as users_views


urlpatterns = [
    ####################################################################################################
    ######################################### READ USERS ###############################################
    ####################################################################################################
    path(
        "",
        users_views.CustomUserListAPIView.as_view(),
        name="list_of_accounts",
    ),
    path(
        "me/",
        users_views.CustomUserDetailAPIView.as_view(),
        name="current-user",
    ),
    path(
        "search/by/phone/",
        users_views.CustomUserSearchByPhoneNumberAPIView.as_view(),
        name="search_account_by_phone_number",
    ),
    path(
        "search/by/email/",
        users_views.CustomUserSearchByEmailAPIView.as_view(),
        name="search_account_by_email",
    ),


    ####################################################################################################
    ################################## REGISTRATION AND AUTHENTICATION #################################
    ####################################################################################################
    path(
        "registration/",
        users_views.CustomUserCreateAPIView.as_view(),
        name="registration",
    ),
    path(
        "login/",
        users_views.LoginAPIView.as_view(),
        name="login",
    ),
    # re_path(
    #     r"^email_reset/confirmation/.*",
    #     users_views.ChangeEmailConfirmationAPIView.as_view(),
    #     name="email_confirmation",
    # ),
    path(
        "update/",
        users_views.CustomUserPatchAPIView.as_view(),
        name="update_account",
    ),
    path(
        "delete",
        users_views.CustomUserDeleteAPIView.as_view(),
        name="delete_user",
    ),
    # path(
    #     "registration/confirmation/code/",
    #     users_views.EmailConfirmationAPIViev.as_view(),
    #     name="registration-confirmation-code",
    # ),
    # re_path(
    #     r"^password_reset/confirmation/[a-zA-Z0-9_]+",
    #     users_views.ResetPasswordAPIView.as_view(),
    #     name="password-reset",
    # ),
    # path(
    #     "change_profile/",
    #     users_views.ChangeUserAPIView.as_view(),
    #     name="change_profile",
    # ),
    # path(
    #     "delete_user/",
    #     users_views.DeleteUserAPIView.as_view(),
    #     name="delete_user",
    # ),
    # path(
    #     "details/<str:pk>/",
    #     users_views.UserProfileDetailAPIView.as_view(),
    #     name="details",
    # ),
    # path(
    #     "follow/<uuid>/",
    #     users_views.FollowAPIView.as_view(),
    #     name="follow",
    # ),
    path(
        "password/update/",
        users_views.CustomUserChangePasswordAPIView.as_view(),
        name="update-password",
    ),
    path(
        "password/reset/",
        users_views.SendRequestToResetCustomUserPasswordAPIView.as_view(),
        name="reset_password_request"
    ),
    path(
        "password/reset/confirmation",
        users_views.CustomUserResetPasswordAPIView.as_view(),
        name="reset_password",
    ),

    ####################################################################################################
    ####################################### CONFIRMATION ###############################################
    ####################################################################################################
    path(
        "registration/confirmation/<str:token>/",
        users_views.CustomUserEmailConfirmationAPIViev.as_view(),
        name="registration_confirmation",
    ),
]