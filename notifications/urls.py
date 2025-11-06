from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'notifications', views.NotificationViewSet, basename='notifications')

urlpatterns = router.urls