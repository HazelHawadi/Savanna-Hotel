from django import forms
from .models import Booking, Room

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'check_in_date', 'check_out_date', 'duration']

    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if duration <= 0:
            raise forms.ValidationError("Duration must be greater than zero.")
        return duration

class AddRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'price', 'image']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

