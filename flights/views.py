from django.shortcuts import render,redirect,get_object_or_404
from .models import Airport,Flight,Passenger,Booking
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def shAirports(request):
    airports = Airport.objects.all()
    return render(request,"flights/fAirports.html",{"airports":airports})


def allFlights(request):
    flights = Flight.objects.all()
    airports = Airport.objects.all()
    return render(request,"flights/indexpage.html",{"flights":flights,"airports":airports})


def showdetails(request,flight_id):
    inc1 = get_object_or_404(Flight,pk=flight_id)
    inc3 = inc1.bookings.select_related('passenger').all()
    return render(request,"flights/details.html",{"info":inc1,"info3":inc3,"length":inc1.capacity-len(inc3)})

def booking(request,flight_id):
    f = get_object_or_404(Flight,pk=flight_id)
    current_count = f.bookings.count()
    context_error = {
        "info": f,
        "length": f.capacity-current_count,
        "d_code": f.destination.code,
        "a_code": f.origin.code
    }
    if request.method == 'POST':
        name = request.POST.get('name','').strip()
        email = request.POST.get('email','').strip()

        if not name or not email:
            context_error["error"] = "All fields are required"
            return render(request, 'flights/booking.html', context_error)
        try:
            validate_email(email)
        except ValidationError:
            context_error["error"]="Please enter a valid email address"
            return render(request, 'flights/booking.html', context_error)
        if len(name) < 3:
            context_error["error"] = "Name must be at least 3 characters"
            return render(request, 'flights/booking.html', context_error)
        if Booking.objects.filter(flight=f, passenger__email = email).exists():
            context_error["error"]="You have already booked a seat on this flight"
            return render(request, 'flights/booking.html', context_error)
        if current_count>=f.capacity:
            context_error["error"] = "No seats available"
            return render(request,'flights/booking.html',context_error)
        passenger , created = Passenger.objects.get_or_create(email=email,defaults={'name': name})
        if not created and passenger.name != name:
            passenger.name = name
            passenger.save()
        new_booking = Booking.objects.create(passenger=passenger,flight=f)

        return redirect('confirmation' , booking_code = new_booking.booking_code)
    return render(request,'flights/booking.html' , context_error)




def confirmation(request,booking_code):
    book = get_object_or_404(Booking,booking_code=booking_code)
    return render(request,"flights/confirmation.html",{"booking":book})

def airport(request,code):
    airport = get_object_or_404(Airport,code=code)
    departures = airport.departures.select_related("destination").all()
    arrivals = airport.arrivals.select_related("origin").all()
    return render(request,"flights/airport.html",{"airport":airport,"code":airport.code,"departures":departures,"arrivals":arrivals})

def managebook(request):
    booking = None
    error = None
    if request.method == "POST":
        code = request.POST.get('code')
        if code:
            try:
                booking = Booking.objects.get(booking_code=code)
            except Booking.DoesNotExist:
                error = "Invalid booking code. Please try again."
        else:
            error = "Please enter your booking code"
    return render(request,"flights/managebook.html",{
        "booking":booking,
        "error":error
    })
def cancel_booking(request,booking_code):
    booking = get_object_or_404(Booking,booking_code=booking_code)
    passenger_name = booking.passenger.name
    flight_info = f"{booking.flight.origin}-{booking.flight.destination}"
    booking.delete()
    messages.success(request, f'Booking for {passenger_name} on flight {flight_info} has been cancelled.')
    return redirect('succeed')

def succeed(request):
    return render(request,'flights/succeed.html')






def special(request):
    flights = Flight.objects.filter(destination__city="Dubai")
    return render(request,'flights/specific.html',{"data":flights})




