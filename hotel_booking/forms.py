from django import forms
from .models import Booking, Room
from django.utils import timezone
from datetime import datetime

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'check_in_date', 'check_out_date', 'guests']

    check_in_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.TextInput(attrs={
            'placeholder': 'YYYY-MM-DD',
            'class': 'form-control'
        })
    )

    check_out_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.TextInput(attrs={
            'placeholder': 'YYYY-MM-DD',
            'class': 'form-control'
        })
    )

    guests = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Number of guests',
            'class': 'form-control'
        })
    )

    def clean_check_in_date(self):
        check_in_date = self.cleaned_data.get('check_in_date')
        if check_in_date < timezone.localdate():
            raise forms.ValidationError("Check-in date cannot be in the past.")
        return check_in_date

    def clean_check_out_date(self):
        check_out_date = self.cleaned_data.get('check_out_date')
        if check_out_date < timezone.localdate():
            raise forms.ValidationError("Check-out date cannot be in the past.")
        return check_out_date

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        # Ensure that the check-out date is after the check-in date
        if check_in_date and check_out_date:
            if check_out_date <= check_in_date:
                raise forms.ValidationError("Check-out date must be after check-in date.")
        
        return cleaned_data

class AddRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'price', 'description', 'available']


