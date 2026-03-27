# ✈️ Airline Reservation System

A Django-based airline reservation web application built for CSS 232 Midterm Project. Users can browse flights, book seats using their name and email, receive a unique booking code, and manage or cancel their reservations — all without authentication.

---

## 📁 Project Structure

```
airline_system/
├── airline_system/          # Project configuration
│   ├── settings.py
│   ├── urls.py              # Root URL config (redirects / → allFlights)
│   ├── wsgi.py
│   └── asgi.py
├── flights/                 # Main application
│   ├── models.py            # Airport, Flight, Passenger, Booking
│   ├── views.py             # All view functions
│   ├── urls.py              # App-level URL patterns
│   ├── admin.py             # Admin panel registration
│   ├── migrations/          # Database migration files
│   ├── templates/
│   │   └── flights/
│   │       ├── indexpage.html       # Home page
│   │       ├── details.html         # Flight detail page
│   │       ├── booking.html         # Booking form page
│   │       ├── confirmation.html    # Booking confirmation page
│   │       ├── managebook.html      # Manage/cancel booking page
│   │       ├── airport.html         # Airport detail page
│   │       ├── fAirports.html       # All airports list
│   │       ├── succeed.html         # Cancellation success page
│   │       └── specific.html        # Special filtered flights page
│   └── static/
│       └── flights/
│           ├── css/                 # Per-page stylesheets
│           └── images/              # Airport photos (JFK, LHR, DXB, etc.)
├── db.sqlite3               # SQLite database
└── manage.py
```

---

## 🗄️ Data Models

### `Airport`
| Field     | Type                        | Notes                        |
|-----------|-----------------------------|------------------------------|
| `code`    | `CharField(max_length=3)`   | Unique 3-letter IATA code    |
| `city`    | `CharField(max_length=100)` | City name                    |
| `details` | `TextField`                 | Optional description         |

### `Flight`
| Field         | Type                    | Notes                              |
|---------------|-------------------------|------------------------------------|
| `origin`      | `ForeignKey(Airport)`   | Related name: `departures`         |
| `destination` | `ForeignKey(Airport)`   | Related name: `arrivals`           |
| `duration`    | `IntegerField`          | Duration in minutes                |
| `capacity`    | `IntegerField`          | Max number of passengers           |

### `Passenger`
| Field   | Type                        | Notes         |
|---------|-----------------------------|---------------|
| `name`  | `CharField(max_length=100)` |               |
| `email` | `EmailField`                | Used as identifier for get_or_create |

### `Booking`
| Field          | Type                      | Notes                                      |
|----------------|---------------------------|--------------------------------------------|
| `passenger`    | `ForeignKey(Passenger)`   | Related name: `bookings`                   |
| `flight`       | `ForeignKey(Flight)`      | Related name: `bookings`                   |
| `booking_code` | `CharField(max_length=8)` | Auto-generated, unique, non-editable       |

#### Booking Code Generation
The `booking_code` is automatically generated in the model's `save()` method using Django's `get_random_string` with uppercase letters and digits. It ensures uniqueness by re-generating if a collision is detected:

```python
def save(self, *args, **kwargs):
    if not self.booking_code:
        new_code = generate_booking_code()
        while Booking.objects.filter(booking_code=new_code).exists():
            new_code = generate_booking_code()
        self.booking_code = new_code
    super().save(*args, **kwargs)
```

---

## 🌐 URL Patterns

| URL | View | Name | Description |
|-----|------|------|-------------|
| `/` | redirect | — | Redirects to all flights |
| `/flights/all/` | `allFlights` | `allFlights` | Home page with all flights and airports |
| `/flights/details/<id>/` | `showdetails` | `details` | Flight detail and passenger list |
| `/flights/booking/<id>/` | `booking` | `booking` | Booking form for a flight |
| `/flights/confirmation/<code>/` | `confirmation` | `confirmation` | Booking confirmation with code |
| `/flights/managebooking/` | `managebook` | `managebooking` | Look up and cancel a booking |
| `/flights/cancel_booking/<code>` | `cancel_booking` | `cancel_booking` | Cancel a specific booking |
| `/flights/airport/<code>/` | `airport` | `airport` | Airport arrivals and departures |
| `/flights/airports/` | `shAirports` | `airportslist` | Full list of all airports |
| `/flights/succeed/` | `succeed` | `succeed` | Cancellation success confirmation |
| `/flights/special/` | `special` | `special` | Flights filtered to Dubai |
| `/admin/` | Django Admin | — | Admin panel |

---

## ⚙️ Views Overview

| View | Method | Description |
|------|--------|-------------|
| `allFlights` | GET | Fetches all flights and airports for the index page |
| `showdetails` | GET | Shows flight info, available seats, and booked passengers |
| `booking` | GET/POST | Handles booking form with validation (name, email, capacity check, duplicate check) |
| `confirmation` | GET | Displays booking confirmation and unique code |
| `managebook` | GET/POST | Looks up a booking by code; displays details or error |
| `cancel_booking` | POST | Deletes a booking and redirects to success page |
| `airport` | GET | Shows arrivals and departures for a specific airport |
| `shAirports` | GET | Lists all airports |
| `succeed` | GET | Cancellation success page |
| `special` | GET | Filters flights with destination city = Dubai |

---

## ✅ Booking Flow (Full Request Cycle)

1. User visits `/flights/all/` → sees list of all flights
2. Clicks 🔍 → goes to `/flights/details/<id>/` → sees capacity and passengers
3. Clicks "Book this Flight" → goes to `/flights/booking/<id>/`
4. Submits name and email → POST is validated:
   - Fields must not be empty
   - Email must be valid format
   - Name must be at least 3 characters
   - No duplicate booking for same email + flight
   - Seat must be available
5. `Passenger` is created or retrieved via `get_or_create(email=...)`
6. `Booking` is created → `booking_code` is auto-generated in `save()`
7. User is redirected to `/flights/confirmation/<code>/`
8. Confirmation page displays the booking code and flight details

---

## 🔧 Setup & Installation

### Requirements
- Python 3.10+
- Django 5.x

### Steps

```bash
# 1. Unzip and navigate into the project
unzip airline_system.zip
cd airline_system

# 2. Install Django
pip install django

# 3. Apply migrations
python manage.py migrate

# 4. (Optional) Create a superuser for admin access
python manage.py createsuperuser

# 5. Run the development server
python manage.py runserver
```

Then open your browser at: **http://127.0.0.1:8000/**

---

## 🗃️ Database

The project uses **SQLite** (`db.sqlite3`) which is included with the submission and pre-populated with:

- **10 Airports** (e.g., JFK, LHR, DXB, CDG, SIN, NRT, HND, LAX, MIA, SYD)
- **21 Flights** across various routes
- Sample bookings for testing

To re-populate via the Django shell:
```bash
python manage.py shell
```
```python
from flights.models import Airport, Flight
Airport.objects.create(code="JFK", city="New York")
# etc.
```

---

## 🛠️ Admin Panel

All models are registered in the Django admin panel.

Access at: **http://127.0.0.1:8000/admin/**

Registered models: `Airport`, `Flight`, `Passenger`, `Booking`

---

## 🎨 Static Files

Each page has its own CSS file under `flights/static/flights/css/`:

| File | Used by |
|------|---------|
| `indexpagestyle.css` | Index / home page |
| `managebooking.css` | Manage booking & booking form |
| `confirm.css` | Booking confirmation page |
| `airports.css` | Airport detail page |
| `manage.css` | Additional manage styles |

Airport photos (`.jpg`) are stored in `flights/static/flights/images/` and are dynamically loaded in templates using the airport's 3-letter code (e.g., `jfk.jpg`, `lhr.jpg`).| `detailsstyle.css` | Flig
Due: March 27, 2026ht details page |
