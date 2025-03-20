from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static  # Import static
from django.contrib.auth import views as auth_views
from hotel_booking import views

urlpatterns = [
    path('', views.home, name='home'),  # Map root URL to home view
    path('admin/', admin.site.urls),
    path('', include('hotel_booking.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Django's built-in auth URLs for login/logout
    path("accounts/", include("accounts.urls")),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Serve static files during development