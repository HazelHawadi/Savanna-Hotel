from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Booking, Room
from django.utils import timezone


class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.room = kwargs.pop('room', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'guests']

    check_in_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.TextInput(attrs={
            'placeholder': 'DD/MM/YYYY',
            'class': 'form-control'
        })
    )

    check_out_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.TextInput(attrs={
            'placeholder': 'DD/MM/YYYY',
            'class': 'form-control'
        })
    )

    guests = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Number of guests',
            'class': 'form-control'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in_date')
        check_out = cleaned_data.get('check_out_date')
        guests = cleaned_data.get('guests')

        if not check_in or not check_out or not self.room:
            return cleaned_data

        overlapping_bookings = Booking.objects.filter(
            room=self.room,
            check_in_date__lt=check_out,
            check_out_date__gt=check_in
        )
        if overlapping_bookings.exists():
            raise ValidationError("This room is already booked during the selected dates.")

        if guests and guests > self.room.capacity:
            raise ValidationError(
                f"This room has a maximum capacity of {self.room.capacity} guests."
            )

        return cleaned_data
    

class BookingUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.room = kwargs.pop('room', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'guests']

    check_in_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.TextInput(
            attrs={
                'placeholder': 'DD/MM/YYYY',
                'class': 'form-control'
            }
        )
    )

    check_out_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.TextInput(
            attrs={
                'placeholder': 'DD/MM/YYYY',
                'class': 'form-control'
            }
        )
    )

    guests = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Number of guests',
                'class': 'form-control'
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in_date')
        check_out = cleaned_data.get('check_out_date')
        guests = cleaned_data.get('guests')
        room = self.room or self.instance.room

        if guests and room and guests > room.capacity:
            raise ValidationError(
                f"This room has a maximum capacity of {room.capacity} guests."
            )

        return cleaned_data

    def clean_check_in_date(self):
        check_in_date = self.cleaned_data.get('check_in_date')
        today = timezone.localdate()

        if check_in_date < today:
            raise forms.ValidationError(
                "Check-in date cannot be in the past."
            )
        return check_in_date

    def clean_check_out_date(self):
        check_out_date = self.cleaned_data.get('check_out_date')
        check_in_date = self.cleaned_data.get('check_in_date')
        today = timezone.localdate()

        if check_out_date < today:
            raise forms.ValidationError(
                "Check-out date cannot be in the past."
            )

        if check_out_date <= check_in_date:
            raise forms.ValidationError(
                "Check-out date must be after the check-in date."
            )
        return check_out_date


class ProfileUpdateForm(forms.ModelForm):
    """Form to update user profile details."""
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class UserDeleteForm(forms.Form):
    """Confirmation form for deleting the user account."""
    confirm = forms.BooleanField(
        label="I confirm that I want to delete my account."
    )


class AddRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'price', 'description', 'available']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
