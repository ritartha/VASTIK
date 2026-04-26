# VASTIK — Full-Stack Second Life Store Website

A Django-based e-commerce showcase for a Second Life store with Indian cultural theming, dark+gold UI inspired by the reference design.

---

## Design Direction (from Reference Image)

The reference image shows a **dark-themed landing page** with:
- Deep dark purple/navy background (#1a1035-ish)
- Vibrant **gold/saffron accent** colors for CTAs and highlights
- Large hero section with atmospheric imagery
- Card-based content sections with subtle gradients
- Clean navigation bar with gold accent button
- Footer with multi-column layout

**Our adaptation**: Same dark+gold aesthetic but with **Indian cultural motifs** — mandala SVGs, lotus elements, ornamental borders, Cinzel/Lato typography.

### Color Palette
| Token | Value | Usage |
|-------|-------|-------|
| `--bg-primary` | `#0F0A1E` | Main background (deep indigo-black) |
| `--bg-secondary` | `#1A1232` | Card/section backgrounds |
| `--bg-tertiary` | `#241B3D` | Elevated surfaces |
| `--accent-gold` | `#F5A623` | Primary accent (saffron/gold) |
| `--accent-crimson` | `#8B1A1A` | Secondary accent (deep crimson) |
| `--text-primary` | `#FFF8ED` | Ivory text |
| `--text-secondary` | `#B8A9C9` | Muted text |
| `--border-gold` | `#C8860A` | Gold borders/dividers |

---

## Project Structure

```
VASTIK/
├── backend/
│   ├── vastik/                    # Django project package
│   │   ├── __init__.py
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py            # Shared settings
│   │   │   ├── development.py     # Dev overrides
│   │   │   └── production.py      # Prod overrides
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── store/                     # Products app
│   │   ├── models.py              # Product, ProductImage
│   │   ├── serializers.py
│   │   ├── views.py               # CBVs + API ViewSets
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── fixtures/
│   │       └── sample_products.json
│   ├── gallery/                   # Gallery app
│   │   ├── models.py              # GalleryImage
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   ├── contact/                   # Contact/OTP app
│   │   ├── models.py              # ContactMessage
│   │   ├── serializers.py
│   │   ├── views.py               # OTP send/verify/submit
│   │   ├── urls.py
│   │   └── admin.py
│   ├── accounts/                  # Auth/admin customization
│   │   ├── admin.py
│   │   └── management/
│   │       └── commands/
│   │           └── load_sample_data.py
│   ├── templates/
│   │   ├── base.html
│   │   └── index.html
│   └── manage.py
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css          # Full design system
│   │   ├── js/
│   │   │   └── main.js            # Vanilla JS (API calls, slideshow, OTP, lightbox)
│   │   └── images/
│   │       ├── mandala.svg
│   │       ├── lotus.svg
│   │       └── hero-bg.webp       # Generated hero image
│   └── templates/                 # (templates served from backend/templates)
├── .env.example
├── .env
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── .gitignore
└── README.md
```

> [!IMPORTANT]
> Templates will live in `backend/templates/` and static files in `frontend/static/`. Django's `STATICFILES_DIRS` will point to `frontend/static/`. This keeps frontend assets separate while Django serves everything.

---

## Proposed Changes

### 1. Project Configuration

#### [NEW] requirements.txt
Django 5.x, djangorestframework, psycopg2-binary, Pillow, django-cors-headers, django-environ, whitenoise, gunicorn

#### [NEW] .env.example
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:pass@localhost:5432/vastik_db
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:8000
```

#### [NEW] docker-compose.yml
PostgreSQL 15 service + Django web service

#### [NEW] Dockerfile
Python 3.11 slim, install requirements, collectstatic, gunicorn

---

### 2. Django Settings (Split Configuration)

#### [NEW] backend/vastik/settings/base.py
- django-environ for `.env` parsing
- All apps registered (store, gallery, contact, accounts, rest_framework, corsheaders)
- Whitenoise middleware for static files
- STATICFILES_DIRS pointing to `frontend/static/`
- TEMPLATES pointing to `backend/templates/`
- MEDIA config for uploads
- REST_FRAMEWORK default settings (pagination, permissions)

#### [NEW] backend/vastik/settings/development.py
- DEBUG=True, SQLite fallback option, console email backend

#### [NEW] backend/vastik/settings/production.py
- DEBUG=False, proper ALLOWED_HOSTS, PostgreSQL enforced, security middleware

---

### 3. Store App

#### [NEW] backend/store/models.py
- `Product` model: serial_number (unique), name, category (Mesh/Script/Texture), description, price, marketplace_url, inworld_slurl, is_featured, created_at
- `ProductImage` model: FK to Product, image (ImageField), order (int)

#### [NEW] backend/store/serializers.py
- `ProductImageSerializer` — nested image serializer
- `ProductSerializer` — includes nested images, category display

#### [NEW] backend/store/views.py
- `ProductListView` (ListAPIView) — filterable by category via query param
- `ProductDetailView` (RetrieveAPIView)
- Consistent JSON response wrapper: `{"success": true, "data": {...}}`

#### [NEW] backend/store/admin.py
- `ProductImageInline` (TabularInline)
- `ProductAdmin` with list_display, list_filter, search_fields

#### [NEW] backend/store/fixtures/sample_products.json
6 products (VTK-001 to VTK-006), 2 per category

---

### 4. Gallery App

#### [NEW] backend/gallery/models.py
- `GalleryImage`: title, image, uploaded_at, is_visible

#### [NEW] backend/gallery/serializers.py
- `GalleryImageSerializer`

#### [NEW] backend/gallery/views.py
- `GalleryListView` — returns only visible images

#### [NEW] backend/gallery/admin.py
- List with thumbnail preview, is_visible toggle

---

### 5. Contact/OTP App

#### [NEW] backend/contact/models.py
- `ContactMessage`: sl_name, topic (choices), message, otp_code, otp_verified, otp_created_at, submitted_at, is_read

#### [NEW] backend/contact/serializers.py
- `SendOTPSerializer` — validates sl_name
- `VerifyOTPSerializer` — validates sl_name + otp_code
- `SubmitContactSerializer` — validates token + topic + message

#### [NEW] backend/contact/views.py
- `SendOTPView` — generates 6-digit OTP, stores with 10-min expiry, prints to console
- `VerifyOTPView` — validates OTP, returns signed token (Django signing module)
- `SubmitContactView` — validates token, saves message

#### [NEW] backend/contact/admin.py
- List with sl_name, topic, submitted_at, is_read
- Bulk "mark as read" action

---

### 6. URL Configuration

#### [NEW] backend/vastik/urls.py
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/products/', include('store.urls')),
    path('api/v1/gallery/', include('gallery.urls')),
    path('api/v1/contact/', include('contact.urls')),
    path('', views.index, name='home'),
]
```

---

### 7. Frontend — Templates

#### [NEW] backend/templates/base.html
- HTML5 boilerplate with meta tags, Google Fonts (Cinzel + Lato)
- Font Awesome CDN
- Links to style.css and main.js
- SEO meta tags

#### [NEW] backend/templates/index.html
All sections in one scrollable page:
1. **Navbar** — Sticky, dark bg, gold accent, hamburger on mobile
2. **Hero** — Full-width with generated Indian-themed background, large "VASTIK" title, tagline, two CTA buttons
3. **About** — Three icon cards (Mesh/Scripts/Textures) with descriptions
4. **Store** — Category filter tabs, responsive product card grid with image slideshow, serial badge, price in L$, two action buttons
5. **Gallery** — Masonry-style grid, lightbox on click (vanilla JS)
6. **Socials** — Centered icons (Facebook, Discord, Instagram, Flickr, SL Profile)
7. **Contact** — Multi-step OTP form (3 steps with progress indicator)
8. **Footer** — Logo, quick links, social icons, copyright

---

### 8. Frontend — CSS

#### [NEW] frontend/static/css/style.css
Complete design system:
- CSS custom properties (color tokens above)
- Dark theme throughout matching reference image aesthetic
- Ornamental gold borders and mandala dividers
- Card hover effects with gold glow
- Smooth scroll behavior
- Responsive breakpoints (mobile-first)
- Animations: fade-in on scroll, slide-up for cards, glow pulse for CTAs
- Lightbox styles
- Multi-step form styles with step indicators
- Hamburger menu animation

---

### 9. Frontend — JavaScript

#### [NEW] frontend/static/js/main.js
Vanilla JS handling:
- **API calls**: Fetch products from `/api/v1/products/`, gallery from `/api/v1/gallery/`
- **Category filtering**: Tab-based filter with AJAX
- **Image slideshow**: Auto-advance with dot indicators on product cards
- **Lightbox**: Click-to-expand gallery images with keyboard nav
- **OTP flow**: Multi-step form state management, POST requests, loading states
- **Smooth scroll**: Navbar link scrolling
- **Hamburger menu**: Mobile nav toggle
- **Scroll animations**: IntersectionObserver for fade-in effects
- **Sticky navbar**: Background change on scroll

---

### 10. Assets

#### [GENERATE] frontend/static/images/hero-bg.webp
Indian-themed hero background image with dark tones

#### [NEW] frontend/static/images/mandala.svg
Decorative mandala SVG for dividers and logo

#### [NEW] frontend/static/images/lotus.svg
Lotus SVG for bullet points and decorative use

---

### 11. Management Command

#### [NEW] backend/accounts/management/commands/load_sample_data.py
- Creates 6 sample products with placeholder images
- Creates 4 sample gallery images
- Prints success message

---

### 12. Documentation

#### [NEW] README.md
Setup instructions: clone, venv, .env config, migrations, sample data, dev server

---

## OTP Verification Flow

```mermaid
sequenceDiagram
    participant U as User (Browser)
    participant S as Django Server
    
    U->>S: POST /api/v1/contact/send-otp/ {sl_name}
    S->>S: Generate 6-digit OTP, store with 10-min expiry
    S->>S: Print OTP to console (simulate SL IM)
    S-->>U: {"success": true, "data": {"message": "OTP sent"}}
    
    U->>S: POST /api/v1/contact/verify-otp/ {sl_name, otp_code}
    S->>S: Validate OTP within expiry window
    S->>S: Generate signed token (django.core.signing)
    S-->>U: {"success": true, "data": {"token": "signed_token"}}
    
    U->>S: POST /api/v1/contact/submit/ {token, topic, message}
    S->>S: Unsign token, get sl_name
    S->>S: Save ContactMessage with submitted_at
    S-->>U: {"success": true, "data": {"message": "Submitted"}}
```

---

## Verification Plan

### Automated Tests
1. Run `python manage.py check` — no errors
2. Run `python manage.py makemigrations --check` — no pending migrations
3. Run `python manage.py migrate` — successful
4. Run `python manage.py load_sample_data` — loads fixtures
5. Run dev server and test all API endpoints via browser:
   - `GET /api/v1/products/`
   - `GET /api/v1/products/?category=Mesh`
   - `GET /api/v1/gallery/`
   - `POST /api/v1/contact/send-otp/`
   - `POST /api/v1/contact/verify-otp/`
   - `POST /api/v1/contact/submit/`

### Manual Verification
- Open `http://localhost:8000` in browser and verify:
  - All sections render correctly
  - Category filter works
  - Gallery lightbox works
  - OTP multi-step form works end-to-end
  - Mobile responsive layout
  - Animations and hover effects

---

## Open Questions

> [!IMPORTANT]
> **PostgreSQL availability**: Do you have PostgreSQL installed locally, or should I configure SQLite as the default for development? The plan includes PostgreSQL in docker-compose, but for immediate local dev, SQLite might be simpler.

> [!NOTE]
> **Social media URLs**: The socials section needs placeholder URLs. I'll use `#` placeholders — you can update them later in Django settings or the template.
