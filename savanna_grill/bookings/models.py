from django.db import models

# Create your models here.
class Booking(models.Model):
    # A field to store the name of the person making the booking
    name = models.CharField(max_length=100)  #limit of 100 characters
    
    # A field to store the date of the booking
    date = models.DateField()
    
    # A field to store the time of the booking
    time = models.TimeField() 
    
    # A field to store the number of guests for the booking
    guests = models.PositiveIntegerField()

    # A method that defines how to show the booking information as a string
    def __str__(self):
        return f"{self.name} - {self.date} @ {self.time}"