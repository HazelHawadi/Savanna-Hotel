from django import forms
from django.contrib.auth.models import User
from .models import Booking, Room
from django.utils import timezone


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'check_in_date', 'check_out_date', 'guests']

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

    def clean_check_in_date(self):
        check_in_date = self.cleaned_data.get('check_in_date')
        if check_in_date < timezone.localdate():
            raise forms.ValidationError(
                "Check-in date cannot be in the past."
            )
        return check_in_date

    def clean_check_out_date(self):
        check_out_date = self.cleaned_data.get('check_out_date')
        check_in_date = self.cleaned_data.get('check_in_date')
        if check_out_date < timezone.localdate():
            raise forms.ValidationError(
                "Check-out date cannot be in the past."
            )
        if check_out_date <= check_in_date:
            raise forms.ValidationError(
                "Check-out date must be after check-in date."
            )
        return check_out_date

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        if check_in_date and check_out_date:
            if check_out_date <= check_in_date:
                raise forms.ValidationError(
                    "Check-out date must be after check-in date."
                )
        return cleaned_data

    def clean_guests(self):

        guests = self.cleaned_data.get('guests')
        room = self.cleaned_data.get('room')

        if room and guests:
            if guests > room.capacity:
                raise forms.ValidationError(
                    "The number of guests exceeds the room's capacity."
                )

        return guests


class BookingUpdateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'check_in_date', 'check_out_date', 'guests']

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
