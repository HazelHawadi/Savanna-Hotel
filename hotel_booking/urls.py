from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import custom_login

app_name = 'hotel_booking'  #  defines the namespace

urlpatterns = [
    path('', views.index, name='index'),  
    path('room/<int:room_id>/', views.room_details, name='room_details'),
    path('add_room/', views.add_room, name='add_room'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('accounts/login/', views.custom_login, name='login'),
    path("login/", custom_login, name="login"),
    path('register/', views.register, name='register'),  # Register URL
    path('logout/', views.custom_logout, name='logout'),
    path('hotel-booking/', views.hotel_booking_view, name='hotel_booking'),
    
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)