from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'admin/attire', views.AttireAdminViewSet, basename='admin_attire')
router.register(r'attire', views.AttireUserViewSet, basename='user_attire')


urlpatterns = router.urls