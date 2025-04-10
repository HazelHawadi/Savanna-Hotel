from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal  # Import Decimal
from hotel_booking.models import Booking


def register_view(request):
    """Handle user registration"""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, "Registration successful! Welcome."
            )  # Break long line
            return redirect("home")
        else:
            messages.error(
                request, "Registration failed. Please correct the errors."
            )  # Break long line
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    """Handle user login with 'Remember Me' functionality"""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(
                    request, f"Welcome back, {user.username}!"
                )  # Break long line

                # Check if 'Remember Me' was checked
                if request.POST.get('remember_me'):
                    request.session.set_expiry(365 * 24 * 60 * 60)
                else:
                    request.session.set_expiry(0)

                return redirect("home")
            else:
                messages.error(
                    request, "Invalid username or password."
                )  # Break long line
        else:
            messages.error(
                request, "Invalid credentials. Please try again."
            )  # Break long line
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    """Logout the user"""
    logout(request)
    return redirect("hotel_booking:index")


def my_bookings(request):
    """Display user's bookings"""
    bookings = Booking.objects.filter(user=request.user)

    for booking in bookings:
        if booking.total_cost is None:
            booking.total_cost = Decimal('0.00')

    return render(request, 'accounts/my_bookings.html', {'bookings': bookings})
