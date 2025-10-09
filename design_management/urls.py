from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('designs', views.ManageDesignViewSet, basename='designs')
router.register('user_designs', views.UserDesignsViewSet, basename='user_designs')

urlpatterns = router.urls