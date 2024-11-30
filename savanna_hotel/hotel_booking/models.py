from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)  
    image = models.ImageField(upload_to='rooms/', default='rooms/default_image.jpg')
    available = models.BooleanField(default=True)

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    duration = models.PositiveIntegerField()  # Duration in nights
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking by {self.name} for {self.room.name}"