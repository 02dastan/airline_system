from django.db import models
import uuid
class Airport(models.Model):
    code = models.CharField(max_length=3,unique=True)
    city = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.city}({self.code})"
class Flight(models.Model):
    origin = models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="departures")
    destination = models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="arrivals")
    duration = models.IntegerField(help_text="duration in minutes")
    capacity = models.IntegerField()
    def __str__(self):
        return f"{self.origin}{self.destination}({self.duration}min){self.capacity}"
class Passenger(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    def __str__(self):
        return f"{self.name}{self.email}"
class Booking(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='bookings')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='bookings')
    booking_code = models.CharField(max_length=36, unique=True, default=uuid.uuid4, editable=False)
    def __str__(self):
        return f"{self.booking_code}{self.flight}{self.passenger}"