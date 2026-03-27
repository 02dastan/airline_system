import string
from django.db import models
from django.utils.crypto import get_random_string

#.all()
#.filter()
#.exclude(id=1)
#.get(id=1)
#.create()
#.get_or_create()
#.filter().update()
#.filter().delete()
#.order_by()
#.count
#filter().exist()
# .first()  .last()

def generate_booking_code():
    length = 8
    allowed_chars = string.ascii_uppercase+string.digits
    return get_random_string(length,allowed_chars)




class Airport(models.Model):
    code = models.CharField(max_length=3,unique=True)
    city = models.CharField(max_length=100)
    details = models.TextField(null=True,blank=True)
    def __str__(self):
        return f"{self.city} | ({self.code})"





class Flight(models.Model):
    origin = models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="departures")
    destination = models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="arrivals")
    duration = models.IntegerField(help_text="duration in minutes")
    capacity = models.IntegerField()
    def __str__(self):
        return f"{self.origin} | {self.destination} | ({self.duration}min) | {self.capacity}"




        
class Passenger(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    def __str__(self):
        return f"{self.name} | {self.email}"


class Booking(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='bookings')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='bookings')
    booking_code = models.CharField(max_length=8, unique=True, editable=False)
    def save(self,*args, **kwargs):
        if not self.booking_code:
            new_code= generate_booking_code()
            while Booking.objects.filter(booking_code=new_code).exists():
                new_code=generate_booking_code()
            self.booking_code= new_code
        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.booking_code} | {self.flight} | {self.passenger}"