# VASTIK — Where Indian Art Meets the Metaverse

A full-stack Django website for the **VASTIK** Second Life store, selling premium Mesh, Scripts, and Textures with an Indian cultural theme.

![VASTIK](frontend/static/images/hero-bg.png)

## Tech Stack

- **Backend:** Django 5.x, Django REST Framework
- **Database:** PostgreSQL 15+ (SQLite for development)
- **Frontend:** Vanilla HTML/CSS/JS with Indian cultural design
- **Static Files:** WhiteNoise
- **Image Handling:** Pillow
- **Environment:** django-environ

## Quick Setup

### 1. Clone & Create Virtual Environment

```bash
git clone <your-repo-url>
cd VASTIK

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings (or use defaults for development)
```

The default `.env` uses SQLite for development. To use PostgreSQL, uncomment the `DATABASE_URL` line.

### 4. Run Migrations

```bash
cd backend
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Load Sample Data

```bash
python manage.py load_sample_data
```

This creates 6 sample products (2 Mesh, 2 Script, 2 Texture) and 4 gallery images.

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit:
- **Website:** http://localhost:8000
- **Admin:** http://localhost:8000/admin/
- **API:** http://localhost:8000/api/v1/products/

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/products/` | List all products |
| GET | `/api/v1/products/<id>/` | Product detail |
| GET | `/api/v1/products/?category=Mesh` | Filter by category |
| GET | `/api/v1/gallery/` | Gallery images |
| POST | `/api/v1/contact/send-otp/` | Send OTP (accepts `{sl_name}`) |
| POST | `/api/v1/contact/verify-otp/` | Verify OTP (accepts `{sl_name, otp_code}`) |
| POST | `/api/v1/contact/submit/` | Submit message (accepts `{token, topic, message}`) |

All API responses follow the format:
```json
{ "success": true, "data": {...} }
{ "success": false, "error": "..." }
```

## OTP Verification Flow

1. User enters their SL Name → Server generates a 6-digit OTP
2. OTP is printed to the Django console (simulates SL IM delivery)
3. User enters the OTP → Server validates and returns a signed token
4. User submits their message with the token

> **Note:** In production, integrate with an SL bot or email service for OTP delivery.

## Docker Setup

```bash
docker-compose up --build
```

This starts PostgreSQL and the Django application.

## Project Structure

```
VASTIK/
├── backend/
│   ├── vastik/          # Django project settings
│   ├── store/           # Products app
│   ├── gallery/         # Gallery app
│   ├── contact/         # Contact/OTP app
│   ├── accounts/        # Admin/auth + management commands
│   ├── templates/       # HTML templates
│   └── manage.py
├── frontend/
│   └── static/
│       ├── css/         # Design system
│       ├── js/          # Vanilla JavaScript
│       └── images/      # SVGs and hero image
├── .env.example
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## License

© 2025 VASTIK — All rights reserved.
Designed for Second Life Residents.
