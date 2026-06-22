# FreelanceKE API 🇰🇪
> A hyperlocal freelance marketplace backend built for East Africa

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)
![DRF](https://img.shields.io/badge/DRF-3.15-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

# What Is This

FreelanceKE is a REST API backend powering a hyperlocal freelance marketplace designed for the Kenyan gig economy. Freelancers — designers, developers, photographers, writers, and errand runners — can list their services, receive bookings from clients, and get paid via M-Pesa simulation. Kenya has one of the fastest-growing freelance communities in Africa, yet most existing platforms are built for Western markets with payment systems that don't reflect local reality. FreelanceKE is built from the ground up with the Kenyan context in mind — M-Pesa as the default payment method, county-based location filtering, and a role system that maps to how work actually gets done here.\

## Features
- JWT Authentication with role-based access (Freelancer, Client, Admin)
- M-Pesa payment simulation with transaction tracking
- Real-time notifications via Django Signals
- Advanced filtering, search, and cursor pagination on service listings
- File uploads for service portfolio images
- Comprehensive test suite — 21 tests, 100% passing

## Architecture

```
Client (Flutter/Postman)
        ↓
   JWT Auth Layer
        ↓
   DRF ViewSets + Router
        ↓
┌──────────────────────────┐
│  accounts │ services     │
│  bookings │ payments     │
│  reviews  │ notifications│
└──────────────────────────┘
        ↓
   Django ORM + Signals
        ↓
   PostgreSQL (prod)
   SQLite (dev)
```

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Get JWT tokens | No |
| POST | `/api/auth/refresh/` | Refresh access token | No |
| GET | `/api/services/` | List all services | No |
| POST | `/api/services/` | Create service | Freelancer |
| POST | `/api/services/{id}/toggle-availability/` | Toggle service | Owner |
| GET | `/api/freelancers/{id}/earnings-summary/` | Earnings data | Auth |
...

## Local Setup

\```bash
git clone https://github.com/ansari-devhub/freelanceke.git
cd freelanceke
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
\```

Create a `.env` file:
\```
SECRET_KEY=your-secret-key
DEBUG=True
\```

\```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
\```

## Tests
\```bash
python manage.py test tests
\```
21 tests covering authentication, service CRUD, booking lifecycle,
permission boundaries, and signal behavior.

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Language | Python 3.12 |
| Framework | Django 5.0 + DRF 3.15 |
| Auth | SimpleJWT |
| Filtering | django-filter |
| Database | PostgreSQL (prod) / SQLite (dev) |
| Deployment | Railway |