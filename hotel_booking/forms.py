from django import forms
from .models import Booking, Room
from django.utils import timezone

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'check_in_date', 'check_out_date']

    def clean_check_in_date(self):
        check_in_date = self.cleaned_data.get('check_in_date')
        if check_in_date and check_in_date < timezone.now().date():
            raise forms.ValidationError("Check-in date cannot be in the past.")
        return check_in_date

    def clean_check_out_date(self):
        check_out_date = self.cleaned_data.get('check_out_date')
        check_in_date = self.cleaned_data.get('check_in_date')

        if check_out_date and check_out_date < timezone.now().date():
            raise forms.ValidationError("Checkout date cannot be in the past.")
        
        if check_in_date and check_out_date and check_out_date <= check_in_date:
            raise forms.ValidationError("Checkout date must be later than check-in date.")
        
        return check_out_date

class AddRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'price', 'description', 'available']
