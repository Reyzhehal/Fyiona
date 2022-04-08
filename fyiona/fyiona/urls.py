from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static



urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/accounts/", include("users.urls")),
    path("api/v1/posts/", include("posts.urls")),
    # path("api/v1/stories/", include("stories.urls")),
    # path("api/v1/messages/", include("umessages.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
