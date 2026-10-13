# Restaurant API

A Django REST Framework backend for a restaurant ordering system with role-based accounts, menu management, cart operations, and food reviews.

## Overview

This project exposes a REST API for a restaurant application where:

- customers can create accounts and place items in a cart
- staff accounts can manage menu categories and food items
- admin users can manage roles and approve staff accounts
- public users can browse active menu items and approved reviews
- authenticated users can submit and view reviews

## Tech stack

- Python 3
- Django 6.1
- Django REST Framework
- PostgreSQL
- JWT authentication with Simple JWT
- Django Filters
- CORS headers
- Swagger / ReDoc via drf-yasg

## Features

- Role-based access control for CUSTOMER, STAFF, and ADMIN users
- JWT login and token refresh flow
- User registration for customer, staff, and admin accounts
- Staff approval workflow before a staff account can log in
- Menu categories and food items with availability checks
- Cart management with add, update, and remove item actions
- Review creation, approval, filtering, and search
- Pagination and filtering support across list endpoints
- Swagger documentation at runtime

## Project structure

```text
restaurant_api/
├── README.md
├── venv/
└── config/
    ├── accounts/
    ├── cart/
    ├── config/
    ├── menu/
    ├── reviews/
    ├── manage.py
    ├── requirements.txt
    └── media/
```

> The Django project root is the `config/` directory.

## Prerequisites

Before you start, make sure the following are installed:

- Python 3.10+
- PostgreSQL server
- pip
- virtualenv (optional but recommended)

## Setup

### 1) Clone the project

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

### 4) Create environment variables

Create a `.env` file inside the Django project root (`config/.env`) with values similar to:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=restaurant_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

The project reads these values in `config/config/settings.py` using `python-decouple`.

### 5) Create the PostgreSQL database

Make sure PostgreSQL is running and a database exists:

```sql
CREATE DATABASE restaurant_db;
```

### 6) Run database migrations

```bash
cd config
python manage.py migrate
```

### 7) Create a superuser

```bash
python manage.py createsuperuser
```

### 8) Start the development server

```bash
python manage.py runserver 0.0.0.0:8000
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## API documentation

The project includes OpenAPI docs:

- Swagger UI: `http://127.0.0.1:8000/swagger/`
- ReDoc: `http://127.0.0.1:8000/redoc/`
- JSON schema: `http://127.0.0.1:8000/swagger.json`

## Authentication

Authentication is handled with JWT. The project uses `rest_framework_simplejwt` and `JWTAuthentication`.

### Login

```http
POST /api/auth/login/
Content-Type: application/json
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
  "refresh": "<refresh-token>",
  "access": "<access-token>",
  "username": "admin",
  "role": "ADMIN"
}
```

### Refresh token

```http
POST /api/token/refresh/
Content-Type: application/json
```

```json
{
  "refresh": "<refresh-token>"
}
```

### Authorization header

```http
Authorization: Bearer <access-token>
```

## Core API endpoints

### Authentication and users

| Method | Endpoint                       | Description                       |
| ------ | ------------------------------ | --------------------------------- |
| POST   | `/api/auth/register/customer/` | Register a customer               |
| POST   | `/api/auth/register/staff/`    | Register a staff member           |
| POST   | `/api/auth/register/admin/`    | Register an admin                 |
| POST   | `/api/auth/login/`             | Login and receive JWT tokens      |
| GET    | `/api/auth/profile/`           | View the logged-in user profile   |
| PATCH  | `/api/auth/profile/`           | Update the logged-in user profile |
| GET    | `/api/auth/users/`             | List users (admin only)           |
| PATCH  | `/api/auth/users/<id>/role/`   | Update a user role (admin only)   |
| POST   | `/api/token/refresh/`          | Refresh the JWT access token      |

Example customer registration:

```http
POST /api/auth/register/customer/
Content-Type: application/json
```

```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "phone": "9800000000",
  "password": "secret123",
  "password1": "secret123"
}
```

### Menu

| Method | Endpoint                     | Description                         |
| ------ | ---------------------------- | ----------------------------------- |
| GET    | `/api/menu/categories/`      | List categories                     |
| POST   | `/api/menu/categories/`      | Create a category (staff/admin)     |
| GET    | `/api/menu/categories/<id>/` | Get category details                |
| PATCH  | `/api/menu/categories/<id>/` | Update category (staff/admin)       |
| DELETE | `/api/menu/categories/<id>/` | Soft-delete category (staff/admin)  |
| GET    | `/api/menu/foods/`           | List food items                     |
| POST   | `/api/menu/foods/`           | Create food item (staff/admin)      |
| GET    | `/api/menu/foods/<id>/`      | Get food details                    |
| PATCH  | `/api/menu/foods/<id>/`      | Update food item (staff/admin)      |
| DELETE | `/api/menu/foods/<id>/`      | Soft-delete food item (staff/admin) |

Food items support filtering and search via query parameters such as:

```http
GET /api/menu/foods/?category=1&food_type=VEGETARIAN&search=pizza&ordering=price
```

### Cart

| Method | Endpoint                              | Description                             |
| ------ | ------------------------------------- | --------------------------------------- |
| GET    | `/api/cart/`                          | Get the current user's cart             |
| POST   | `/api/cart/`                          | Create or fetch the current user's cart |
| POST   | `/api/cart/item/`                     | Add an item to the cart                 |
| PATCH  | `/api/cart/update-item/`              | Update cart item quantity               |
| DELETE | `/api/cart/remove-item/?item_id=<id>` | Remove a cart item                      |

Example add item request:

```http
POST /api/cart/item/
Content-Type: application/json
```

```json
{
  "food_item": 1,
  "quantity": 2
}
```

### Reviews

| Method | Endpoint                     | Description                    |
| ------ | ---------------------------- | ------------------------------ |
| GET    | `/api/reviews/`              | List reviews                   |
| POST   | `/api/reviews/`              | Create a review                |
| GET    | `/api/reviews/<id>/`         | Get a review                   |
| PATCH  | `/api/reviews/<id>/`         | Update your own review         |
| DELETE | `/api/reviews/<id>/`         | Delete your own review         |
| POST   | `/api/reviews/<id>/approve/` | Approve a review (staff/admin) |

Approved reviews are visible to the public; staff and admins can view all reviews, while customers can see approved reviews and their own review submissions.

## Role behavior

- CUSTOMER: can register, log in, view own profile, add items to cart, and submit reviews
- STAFF: can manage menu categories and food items; requires admin approval before login
- ADMIN: can manage users, assign roles, and approve staff reviews and staff account access

## Useful commands

Apply migrations:

```bash
cd config
python manage.py makemigrations
python manage.py migrate
```

Run tests:

```bash
python manage.py test
```

Start the development server:

```bash
python manage.py runserver
```

## Notes

- The project uses PostgreSQL by default in `config/config/settings.py`.
- Some endpoints are intentionally restricted by role and authentication.
- For local development, keep the `.env` file out of version control.

## License

This project is intended for learning and local development purposes unless otherwise specified by the project owner.

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
