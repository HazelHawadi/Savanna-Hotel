from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm
from hotel_booking.models import Room


@login_required
def add_review(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.room = room
            review.save()
            return redirect("hotel_booking:room_detail", id=room_id)
    else:
        form = ReviewForm()
    return render(
        request,
        "reviews/edit_review.html",
        {"form": form, "review": review}
    )


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect(
                "hotel_booking:room_detail",
                id=review.room.id
            )
    else:
        form = ReviewForm(instance=review)
    return render(
        request,
        "reviews/edit_review.html",
        {"form": form, "review": review},
    )


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    room_id = review.room.id

    if request.method == "POST":
        review.delete()
        return redirect("hotel_booking:room_detail", id=room_id)

    return render(request, "reviews/delete_review.html", {"review": review})
