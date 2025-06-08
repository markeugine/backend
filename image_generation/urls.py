from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('image', views.ImageGenerationViewset, basename='image')
urlpatterns = router.urls