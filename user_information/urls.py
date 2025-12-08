# urls.py
from rest_framework.routers import DefaultRouter
from .views import UserInformationViewSet

router = DefaultRouter()
router.register(r'user-information', UserInformationViewSet, basename='user-information')

urlpatterns = router.urls