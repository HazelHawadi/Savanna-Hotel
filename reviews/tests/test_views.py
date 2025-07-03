from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from hotel_booking.models import Room
from reviews.models import Review

class ReviewViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.room = Room.objects.create(name="Test Room", description="Nice room", price=100)
        self.client.login(username="testuser", password="testpass")

    def test_add_review_get(self):
        url = reverse("reviews:add_review", args=[self.room.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/add_review.html")
        self.assertIn("form", response.context)

    def test_add_review_post_valid(self):
        url = reverse("reviews:add_review", args=[self.room.id])
        data = {"rating": 5, "comment": "Excellent room!"}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("hotel_booking:room_detail", kwargs={"id": self.room.id}))
        self.assertEqual(Review.objects.count(), 1)
        review = Review.objects.first()
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Excellent room!")
        self.assertEqual(review.user, self.user)

    def test_edit_review_get(self):
        review = Review.objects.create(user=self.user, room=self.room, rating=3, comment="Okay stay")
        url = reverse("reviews:edit_review", args=[review.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/edit_review.html")
        self.assertIn("form", response.context)

    def test_edit_review_post_valid(self):
        review = Review.objects.create(user=self.user, room=self.room, rating=3, comment="Okay stay")
        url = reverse("reviews:edit_review", args=[review.id])
        data = {"rating": 4, "comment": "Improved stay"}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("hotel_booking:room_detail", kwargs={"id": self.room.id}))
        review.refresh_from_db()
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, "Improved stay")

    def test_delete_review_get(self):
        review = Review.objects.create(user=self.user, room=self.room, rating=3, comment="Okay stay")
        url = reverse("reviews:delete_review", args=[review.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/delete_review.html")
        self.assertIn("review", response.context)

    def test_delete_review_post(self):
        review = Review.objects.create(user=self.user, room=self.room, rating=3, comment="Okay stay")
        url = reverse("reviews:delete_review", args=[review.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse("hotel_booking:room_detail", kwargs={"id": self.room.id}))
        self.assertEqual(Review.objects.count(), 0)
