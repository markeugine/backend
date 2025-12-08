from . import views
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ExportDesignsCSV

router = DefaultRouter()
router.register('designs', views.ManageDesignViewSet, basename='designs')
router.register('user_designs', views.UserDesignsViewSet, basename='user_designs')


urlpatterns = [
    path('export/csv/', ExportDesignsCSV.as_view(), name='export_designs_csv'),
]
urlpatterns += router.urls

# Add router URLs at the end
urlpatterns += router.urls