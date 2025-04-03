from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from accounts.views import login_view
from .views import custom_login
from django.conf.urls import handler404

app_name = 'hotel_booking'

handler404 = 'hotel_booking.views.custom_404'

urlpatterns = [
    path('', views.index, name='index'),  
    path('room/<int:room_id>/', views.room_details, name='room_details'),
    path('add_room/', views.add_room, name='add_room'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('create_booking/', views.create_booking, name='create_booking'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('accounts/login/', login_view, name='login'),
    path('register/', views.register, name='register'),  # Register URL
    path('logout/', views.custom_logout, name='logout'),
    path('hotel-booking/', views.hotel_booking_view, name='hotel_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('room/<int:id>/', views.room_details, name='room_detail'),
    path('update/<int:id>/', views.update_booking, name='update_booking'),
    path('delete/<int:id>/', views.delete_booking, name='delete_booking'),
    
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)