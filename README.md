# Restaurant API

A Django REST Framework backend for a restaurant ordering and review system with role-based access, menu management, cart handling, and JWT authentication.

## Features

- Customer, staff, and admin user roles
- JWT-based authentication with refresh support
- Menu categories and food items
- Cart management for authenticated customers
- Review submission and approval workflow
- Filtering, search, ordering, and pagination
- PostgreSQL database support

## Project structure

```text
restaurant_api/
├── config/
│   ├── accounts/
│   ├── cart/
│   ├── config/
│   ├── menu/
│   ├── reviews/
│   ├── manage.py
│   ├── requirements.txt
│   └── db.sqlite3
├── media/
├── venv/
└── README.md
```

> The Django project root is inside the `config` folder.

---

## Installation

### 1) Clone and enter the project

```bash
cd /path/to/restaurant_api
```

### 2) Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r config/requirements.txt
```

### 4) Configure environment variables

Create a `.env` file in the `config` folder with values like:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=restaurant_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

The project uses `python-decouple` and reads these values in `config/config/settings.py`.

### 5) Create the database

Make sure PostgreSQL is running and the database exists.

```bash
cd config
python manage.py migrate
```

### 6) Run the server

```bash
python manage.py runserver 0.0.0.0:8000
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

---

## Database migrations

To apply schema changes:

```bash
cd config
python manage.py makemigrations
python manage.py migrate
```

To create a superuser:

```bash
python manage.py createsuperuser
```

---

## JWT setup and authentication

This project uses `djangorestframework_simplejwt`.

### JWT settings

From `config/config/settings.py`:

```python
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}
```

JWT is enabled globally in DRF:

```python
'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework.authentication.TokenAuthentication',
    'rest_framework.authentication.BasicAuthentication',
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework_simplejwt.authentication.JWTAuthentication',
],
```

### Login and token generation

The app provides a custom login endpoint:

```http
POST /api/auth/login/
```

Request body:

```json
{
  "username": "admin",
  "password": "secret123"
}
```

Example response:

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "username": "admin",
  "role": "ADMIN"
}
```

### Refresh token

```http
POST /api/token/refresh/
```

Request body:

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Example response:

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Authorization header

For protected routes:

```http
Authorization: Bearer <access_token>
```

---

## API endpoints

### 1) Authentication and users

| Method | Endpoint                       | Description                       |
| ------ | ------------------------------ | --------------------------------- |
| POST   | `/api/auth/register/customer/` | Create a customer user            |
| POST   | `/api/auth/register/staff/`    | Create a staff user               |
| POST   | `/api/auth/register/admin/`    | Create an admin user              |
| POST   | `/api/auth/login/`             | Login and get JWT tokens          |
| GET    | `/api/auth/profile/`           | Get logged-in user profile        |
| PATCH  | `/api/auth/profile/`           | Update logged-in user profile     |
| GET    | `/api/auth/users/`             | List users (admin only)           |
| PATCH  | `/api/auth/users/<id>/role/`   | Update a user's role (admin only) |
| POST   | `/api/token/refresh/`          | Refresh access token              |

#### Example: register customer

```http
POST /api/auth/register/customer/
Content-Type: application/json
```

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "phone": "9800000000",
  "password": "secret123",
  "password1": "secret123"
}
```

#### Example: profile response

```json
{
  "id": 1,
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "9800000000",
  "role": "CUSTOMER"
}
```

### 2) Menu

| Method    | Endpoint                     | Description                         |
| --------- | ---------------------------- | ----------------------------------- |
| GET       | `/api/menu/categories/`      | List active categories              |
| POST      | `/api/menu/categories/`      | Create category (staff/admin)       |
| GET       | `/api/menu/categories/<id>/` | Single category                     |
| PUT/PATCH | `/api/menu/categories/<id>/` | Update category (staff/admin)       |
| DELETE    | `/api/menu/categories/<id>/` | Soft delete category (staff/admin)  |
| GET       | `/api/menu/foods/`           | List available foods                |
| POST      | `/api/menu/foods/`           | Create food item (staff/admin)      |
| GET       | `/api/menu/foods/<id>/`      | Get food item                       |
| PUT/PATCH | `/api/menu/foods/<id>/`      | Update food item (staff/admin)      |
| DELETE    | `/api/menu/foods/<id>/`      | Soft delete food item (staff/admin) |

#### Example: list foods with filters

```http
GET /api/menu/foods/?category=1&food_type=VEGETARIAN&search=pizza&ordering=price
```

#### Example: food item response

```json
{
  "id": 5,
  "category": 1,
  "name": "Veggie Supreme",
  "slug": "veggie-supreme",
  "description": "Loaded with vegetables and mozzarella.",
  "price": "420.00",
  "image": null,
  "food_type": "VEGETARIAN",
  "is_available": true,
  "preparation_time": 20,
  "created_at": "2026-10-11T10:12:34Z",
  "updated_at": "2026-10-11T10:12:34Z"
}
```

### 3) Cart

| Method | Endpoint                              | Description                           |
| ------ | ------------------------------------- | ------------------------------------- |
| GET    | `/api/cart/`                          | Get current authenticated user's cart |
| POST   | `/api/cart/`                          | Create or fetch cart                  |
| POST   | `/api/cart/item/`                     | Add item to cart                      |
| PATCH  | `/api/cart/update-item/`              | Update cart item quantity             |
| DELETE | `/api/cart/remove-item/?item_id=<id>` | Remove item from cart                 |

#### Example: add item to cart

```http
POST /api/cart/item/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "food_item": 5,
  "quantity": 2
}
```

#### Example: cart response

```json
{
  "id": 2,
  "items": [
    {
      "id": 10,
      "food_item": 5,
      "food_name": "Veggie Supreme",
      "price": "420.00",
      "quantity": 2,
      "line_total": "840.00",
      "created_at": "2026-10-11T11:20:00Z",
      "updated_at": "2026-10-11T11:20:00Z"
    }
  ],
  "total_items": 2,
  "cart_total": "840.00",
  "created_at": "2026-10-11T11:18:00Z",
  "updated_at": "2026-10-11T11:20:00Z"
}
```

### 4) Reviews

| Method | Endpoint                     | Description                       |
| ------ | ---------------------------- | --------------------------------- |
| GET    | `/api/reviews/`              | List reviews                      |
| POST   | `/api/reviews/`              | Create review                     |
| GET    | `/api/reviews/<id>/`         | Review detail                     |
| PATCH  | `/api/reviews/<id>/`         | Update own review                 |
| DELETE | `/api/reviews/<id>/`         | Delete own review                 |
| POST   | `/api/reviews/<id>/approve/` | Approve review (staff/admin only) |

#### Example: create a review

```http
POST /api/reviews/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "food_item": 5,
  "rating": 5,
  "comment": "Excellent pizza and fast service."
}
```

#### Example: review response

```json
{
  "id": 3,
  "customer": 2,
  "customer_name": "johndoe",
  "food_item": 5,
  "food_name": "Veggie Supreme",
  "rating": 5,
  "comment": "Excellent pizza and fast service.",
  "is_approved": false,
  "created_at": "2026-10-11T12:00:00Z",
  "updated_at": "2026-10-11T12:00:00Z"
}
```

---

## Role-based behavior

- `CUSTOMER` can register, log in, view their own profile, manage their cart, and create reviews
- `STAFF` can manage menu items/categories and approve reviews
- `ADMIN` can manage users, assign roles, and access staff/admin workflows

---

## Best practices

- Always send the JWT in the `Authorization` header as `Bearer <token>`
- Use refresh tokens to rotate access tokens safely
- Keep the `.env` file out of version control
- Use PostgreSQL in development or production instead of SQLite for real workloads
- Validate role checks on the server side before performing admin/staff actions
- Prefer `GET /api/menu/foods/?search=...` and `?ordering=...` for filtered menu queries

---

## Common commands

```bash
# Start the app
cd config
python manage.py runserver

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Check routes
python manage.py check
```

---

## Notes

- Some endpoints are implemented as DRF viewsets with custom actions.
- The project includes throttling for certain endpoints (`login`, `register`, `cart`, and `reviews`).
- Menu category and food soft-delete behavior is implemented by setting `is_active` or `is_available` to false instead of deleting rows.

If you want, I can also generate a more polished version with a table of all routes, sample `curl` commands, and a production-ready `.env.example` file.
