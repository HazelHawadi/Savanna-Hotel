from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static  # Import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hotel-booking/', include('hotel_booking.urls')),  # URL for hotel-booking app
    path('accounts/', include('django.contrib.auth.urls')),  # Django's built-in auth URLs for login/logout
    path('', include('hotel_booking.urls')),  # Django's built-in auth URLs for login/logout
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Serve static files during development