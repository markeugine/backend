from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from .views import ExportAppointmentsCSV

router = DefaultRouter()
router.register('set_appointments', views.SetAppointmentViewSet, basename='set_appointments')
router.register('appointments', views.AppointmentsListViewSet, basename='appointments')
router.register('user_appointments', views.UserAppointmentsViewSet, basename='user_appointments')
router.register('follow_up', views.FollowUpAppointmentViewSet, basename='follow_up')

urlpatterns = [
    path('export/csv/', ExportAppointmentsCSV.as_view(), name='export_appointments_csv'),
]

urlpatterns += router.urls

# Add router URLs at the end
urlpatterns += router.urls