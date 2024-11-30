from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'hotel_booking'  #  defines the namespace

urlpatterns = [
    path('', views.index, name='index'),
    path('room/<int:room_id>/', views.room_details, name='room_details'),
    path('add-room/', views.add_room, name='add_room'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)