from django.urls import path
from .views import *
urlpatterns = [
    path("airports/",shAirports,name = "airportslist"),
    path("all/",allFlights,name = "allFlights"),
    path("details/<int:flight_id>/",showdetails,name = "details"),
    path("booking/<int:flight_id>/",booking,name = "booking"),
    path("confirmation/<str:booking_code>/",confirmation,name = "confirmation"),
    path("airport/<str:code>/",airport,name = "airport"),
    path("managebooking/",managebook,name="managebooking"),
    path("cancel_booking/<str:booking_code>",cancel_booking, name = "cancel_booking"),
    path("succeed/", succeed,name="succeed"),
]