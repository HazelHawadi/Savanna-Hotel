from django.contrib import admin
from django.urls import path, include
from hotel_booking import views  # Ensure you're importing the correct views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hotel-booking/', include('hotel_booking.urls')),
    path('', views.index, name='index'),  # Keep this to show the homepage with rooms
    path('add_room/', views.add_room, name='add_room'),
]