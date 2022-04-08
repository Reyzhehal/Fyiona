from django.contrib import admin
from django.contrib.auth.models import Group

from .models import (
    CustomUser, 
    UserProfile, 
    CustomUserEmailConfirmationToken,
    AccessTokenToUpdateCustomUserFields, 
)


admin.site.unregister(Group)

admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(CustomUserEmailConfirmationToken)
admin.site.register(AccessTokenToUpdateCustomUserFields)