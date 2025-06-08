from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('set_unavailability', views.SetUnavailabilityViewSet, basename='set_unavailability')
router.register('display_unavailability', views.DisplayUnavailabilityViewSet, basename='display_unavailability')

urlpatterns = router.urls