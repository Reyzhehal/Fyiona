from django.urls import path
from .views import StoryViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", StoryViewSet, basename="story")
urlpatterns = router.urls
