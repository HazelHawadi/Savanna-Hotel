from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static  # Import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hotel-booking/', include('hotel_booking.urls')),  # URL for hotel-booking app
    path('accounts/', include('django.contrib.auth.urls')),  # Django's built-in auth URLs for login/logout
    path('', include('hotel_booking.urls', namespace='hotel_booking')),  # Django's built-in auth URLs for login/logout
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Serve static files during development