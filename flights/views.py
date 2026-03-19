from django.shortcuts import render,redirect,get_object_or_404
from .models import Airport,Flight,Passenger,Booking
from django.contrib import messages
# Create your views here.
def shAirports(request):
    airports = Airport.objects.all()
    return render(request,"flights/fAirports.html",{"airports":airports})


def allFlights(request):
    flights = Flight.objects.all()
    airports = Airport.objects.all()
    return render(request,"flights/indexpage.html",{"flights":flights,"airports":airports})


def showdetails(request,flight_id):
    inc1 = get_object_or_404(Flight,pk=flight_id)
    inc2 = Passenger.objects.all()
    inc3 = inc1.bookings.select_related('passenger').all()
    return render(request,"flights/details.html",{"info":inc1,"info2":inc2,"info3":inc3,"length":inc1.capacity-len(inc3)})

def booking(request,flight_id):
    f = get_object_or_404(Flight,pk=flight_id)
    inc3 = f.bookings.select_related('passenger').all()
    if request.method== 'POST':
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        if name and email:
            passenger = Passenger.objects.create(name=name,email=email)
            booking = Booking.objects.create(passenger=passenger,flight=f)
            return redirect('confirmation', booking_code=booking.booking_code)
    return render(request,"flights/booking.html",{"info":f,"length":f.capacity-len(inc3)})


def confirmation(request,booking_code):
    booking = get_object_or_404(Booking,booking_code=booking_code)
    return render(request,"flights/confirmation.html",{"booking":booking})

def airport(request,code):
    airport = get_object_or_404(Airport,code=code)
    departures = airport.departures.select_related("destination").all()
    arrivals = airport.arrivals.select_related("origin").all()
    return render(request,"flights/airport.html",{"airport":airport,"departures":departures,"arrivals":arrivals})

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