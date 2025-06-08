from django.contrib import admin
from django.urls import path, include
from knox import views as knox_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user_auth.urls')), # Custom user authentication urls.
    path('appointment/', include('appointment.urls')), # Appointment API urls.
    path('availability/', include('availability.urls')), # Availability API urls.
    path('generate/', include('image_generation.urls')), # Availability API urls.
    
    path(r'logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path(r'logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path(r'api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)