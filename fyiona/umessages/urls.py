from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, MessageSessionViewSet

router = DefaultRouter()
router.register(
    "sessions",
    MessageSessionViewSet,
    basename="session",
)
router.register(r"", MessageViewSet, basename="message")
urlpatterns = router.urls
