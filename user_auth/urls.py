from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('send-otp', views.SendOTPViewSet, basename='send-otp')  # NEW
router.register('verify-otp', views.VerifyOTPViewSet, basename='verify-otp')  # NEW
router.register('register', views.RegisterViewset, basename='register')
router.register('login', views.LoginViewset, basename='login')
router.register('users', views.AllUserViewSet, basename='users')
router.register('profile', views.UserProfileViewSet, basename='profile')

urlpatterns = router.urls