from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('register', views.RegisterViewset, basename='register')
router.register('login', views.LoginViewset, basename='login')
router.register('users', views.AllUserViewSet, basename='users')
router.register('profile', views.UserProfileViewSet, basename='profile')

urlpatterns = router.urls