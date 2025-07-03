from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from hotel_booking import views

urlpatterns = [
    path('', views.home, name='home'),  # Map root URL to home view
    path('admin/', admin.site.urls),

    path('', include('hotel_booking.urls')),


    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),

    path('reviews/', include('reviews.urls')),
    path('contact/', TemplateView.as_view(template_name="contact_us.html"), name="contact_us"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
