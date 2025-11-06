from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('set_appointments', views.SetAppointmentViewSet, basename='set_appointments')
router.register('appointments', views.AppointmentsListViewSet, basename='appointments')
router.register('user_appointments', views.UserAppointmentsViewSet, basename='user_appointments')
router.register('follow_up', views.FollowUpAppointmentViewSet, basename='follow_up')

urlpatterns = router.urls