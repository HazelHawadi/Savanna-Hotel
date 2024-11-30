from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Welcome to the Savanna Hotel!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hotel-booking/', include('hotel_booking.urls')),
    path('', home_view, name='home'),  
]