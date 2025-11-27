from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('generate', views.ImageGenerationViewset, basename='generate')
urlpatterns = router.urls