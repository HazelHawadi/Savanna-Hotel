from django.apps import AppConfig


class HotelBookingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hotel_booking'

    def ready(self):
        import hotel_booking.signals  # Import signals
