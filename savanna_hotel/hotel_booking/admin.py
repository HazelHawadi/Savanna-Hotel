from django.contrib import admin
from .models import Room

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available')  # Display fields in the list view
    search_fields = ('name',)  # Allow search by name
    list_filter = ('available',)  # Add a filter option for availability

admin.site.register(Room, RoomAdmin)