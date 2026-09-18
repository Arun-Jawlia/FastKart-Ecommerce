# 🛒FastKart: E-Commerce Backend API

A production-oriented **E-Commerce REST API** built with **FastAPI, PostgreSQL, SQLAlchemy, Redis, JWT Authentication, Alembic, and Docker**.

This project is being developed step-by-step to understand how a real-world e-commerce backend is designed, secured, tested, optimized, and deployed.

---

## 🚀 Tech Stack

| Technology         | Purpose                                |
| ------------------ | -------------------------------------- |
| **Python**         | Backend programming language           |
| **FastAPI**        | REST API framework                     |
| **Pydantic**       | Request/response validation            |
| **PostgreSQL**     | Primary relational database            |
| **SQLAlchemy**     | ORM and database access                |
| **Alembic**        | Database migrations                    |
| **Redis**          | Caching and rate limiting              |
| **JWT**            | Authentication                         |
| **Argon2**         | Password hashing                       |
| **Uvicorn**        | ASGI server                            |
| **Pytest**         | Testing                                |
| **Docker**         | Containerization                       |
| **Docker Compose** | Multi-container development/deployment |
| **Nginx**          | Reverse proxy                          |
| **Git/GitHub**     | Version control                        |

---

# ✨ Features

## 🔐 Authentication & Authorization

* User registration
* User login
* JWT-based authentication
* Secure password hashing with Argon2
* Protected routes
* Role-based authorization
* User/Admin roles
* Ownership-based authorization
* Login rate limiting

---

## 👤 User Management

* Create users through registration
* Get current authenticated user
* Admin user management
* Update user profile
* Delete users
* Duplicate email protection
* Password never exposed through API responses

---

## 📦 Product Management

* Create products
* Update products
* Delete products
* Get product details
* Product listing
* Category assignment
* Stock management
* Low-stock threshold

---

## 🗂️ Category Management

* Create categories
* Update categories
* Delete categories
* Get categories
* Category-product relationship

---

## 🔎 Product Search & Filtering

Product browsing supports:

* Pagination
* Name search
* Category filtering
* Minimum price
* Maximum price
* Sorting by:

  * ID
  * Name
  * Price
  * Stock
* Ascending/descending sorting

Example:

```http
GET /products?page=1&limit=20&search=laptop&category_id=2&min_price=30000&max_price=100000&sort_by=price&sort_order=asc
```

---

# 🛒 Cart

Users can:

* Create/get their cart
* Add products
* Update quantity
* Remove products
* Clear cart
* View cart total
* Validate available stock

Cart ownership is enforced so users cannot access another user's cart.

---

# 📋 Orders & Checkout

The backend supports:

* Checkout from cart
* Order creation
* Order items
* Price snapshots
* Product name snapshots
* Order subtotal
* Order total
* Stock deduction
* Cart clearing
* User order history
* Admin order management

### Order Status

```text
PENDING
   ↓
CONFIRMED
   ↓
SHIPPED
   ↓
DELIVERED
```

Cancellation is supported where allowed by the order state.

---

# 📍 Addresses

Users can manage multiple addresses.

Features:

* Create address
* Get addresses
* Get individual address
* Update address
* Delete address
* Default address
* Address ownership validation

Supported fields include:

```text
Full Name
Phone
Address
City
State
Postal Code
Country
Default Address
```

---

# ⭐ Product Reviews

Authenticated customers can review products they have purchased.

Features:

* Rating from 1–5
* Optional comment
* Verified purchase check
* One review per user/product
* Update own review
* Delete own review
* Public product reviews

A user cannot review a product they haven't purchased.

---

# 📦 Inventory Management

Admin inventory management includes:

* Restock product
* Remove stock
* Set stock
* Low-stock products
* Inventory history
* Inventory transaction tracking

Transaction types include:

```text
RESTOCK
SALE
ADJUSTMENT
DAMAGE
RETURN
```

Each inventory transaction stores:

```text
Previous Quantity
Quantity Change
New Quantity
Transaction Type
Reason
Timestamp
```

This provides an audit trail for inventory changes.

---

# 💳 Payments

The project includes a payment architecture with a mock payment provider.

Features:

* Create payment
* Payment verification
* Payment status
* Transaction reference
* Provider payment ID
* Idempotency key
* Order-payment relationship
* Payment amount derived from the order

Payment statuses:

```text
PENDING
SUCCESS
FAILED
CANCELLED
```

### Important Security Principle

The API never trusts a payment amount supplied by the frontend.

The amount is derived from the server-side order:

```text
Order
  ↓
Order Total
  ↓
Payment
```

A real payment gateway can later replace the mock provider.

---

# ⚡ Redis

Redis is used for performance and application infrastructure.

Current use cases:

### Product caching

```text
GET /products/{id}

Request
   ↓
Redis
   │
   ├── HIT → Return cached product
   │
   └── MISS
         ↓
      PostgreSQL
         ↓
       Redis
         ↓
      Response
```

### Rate limiting

Redis counters are used to limit login attempts.

Example:

```text
5 login attempts / minute / IP
```

When the limit is exceeded:

```http
429 Too Many Requests
```

Redis is not used as the source of truth for business data.

**PostgreSQL remains the source of truth.**

---

# 📧 Background Tasks

FastAPI `BackgroundTasks` is used for lightweight post-response operations.

Example:

```text
Checkout
   ↓
Create Order
   ↓
Return Response
   ↓
Background Task
   ↓
Order Confirmation Email
```

The current email implementation is intentionally simple and can later be connected to:

* SMTP
* SendGrid
* Amazon SES
* Other email providers

---

# 🗄️ Database Migrations

Database schema changes are managed with **Alembic**.

Typical workflow:

```bash
alembic revision --autogenerate -m "add product field"
```

Review the migration:

```text
alembic/versions/
```

Apply:

```bash
alembic upgrade head
```

Rollback:

```bash
alembic downgrade -1
```

Alembic is the source of database schema changes instead of relying on:

```python
Base.metadata.create_all()
```

---

# 🏗️ Architecture

The application follows a layered architecture:

```text
Client
  │
  ▼
FastAPI Router
  │
  ▼
Dependencies
(Authentication / Authorization)
  │
  ▼
Pydantic Schema
  │
  ▼
Service Layer
  │
  ▼
SQLAlchemy Model
  │
  ▼
PostgreSQL
```

Redis is used alongside PostgreSQL:

```text
                 FastAPI
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
     PostgreSQL              Redis
     Source of Truth       Cache / Limits
```

---

# 📁 Project Structure

```text
ecommerce-backend/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── dependencies.py
│   │   └── cache_keys.py
│   │
│   ├── database/
│   │   ├── database.py
│   │   ├── base.py
│   │   ├── init_db.py
│   │   └── redis.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   ├── cart_item.py
│   │   ├── order.py
│   │   ├── order_item.py
│   │   ├── address.py
│   │   ├── review.py
│   │   ├── inventory_transaction.py
│   │   └── payment.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── auth.py
│   │   ├── category.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   ├── address.py
│   │   ├── review.py
│   │   ├── inventory.py
│   │   └── payment.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── categories.py
│   │   ├── products.py
│   │   ├── cart.py
│   │   ├── orders.py
│   │   ├── addresses.py
│   │   ├── reviews.py
│   │   ├── inventory.py
│   │   └── payments.py
│   │
│   └── services/
│       ├── user_service.py
│       ├── category_service.py
│       ├── product_service.py
│       ├── cart_service.py
│       ├── order_service.py
│       ├── address_service.py
│       ├── review_service.py
│       ├── inventory_service.py
│       ├── payment_service.py
│       ├── cache_service.py
│       ├── email_service.py
│       └── rate_limit_service.py
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
│   └── README
│
├── tests/
│
├── nginx/
│   └── nginx.conf
│
├── .env
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── requirements.txt
└── README.md
```

---

# ⚙️ Local Setup

## 1. Clone the repository

```bash
git clone https://github.com/Arun-Jawlia/FastKart-Ecommerce
```

```bash
cd FastKart-Ecommerce
```

---

## 2. Create virtual environment

### Windows

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🐘 PostgreSQL Setup

Create a PostgreSQL database:

```sql
CREATE DATABASE ecommerce_db;
```

Create a `.env` file:

```env
APP_NAME=E-Commerce API
APP_VERSION=1.0.0
DEBUG=true

DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/ecommerce_db

JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

REDIS_URL=redis://localhost:6379/0
```

Replace:

```text
postgres
password
```

with your PostgreSQL credentials.

---

# 🔴 Redis Setup

If Redis is installed locally, make sure it is running.

Or use Docker:

```bash
docker run -d --name ecommerce-redis -p 6379:6379 redis:7
```

Verify:

```bash
docker exec -it ecommerce-redis redis-cli ping
```

Expected:

```text
PONG
```

---

# 🗃️ Run Database Migrations

Apply migrations:

```bash
alembic upgrade head
```

Check current migration:

```bash
alembic current
```

---

# ▶️ Run the Application

```bash
uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# ❤️ Health Checks

Application:

```http
GET /health
```

Database:

```http
GET /health/db
```

Redis:

```http
GET /health/redis
```

---

# 🧪 Testing

Run all tests:

```bash
pytest
```

Verbose:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/test_auth.py -v
```

---

# 🐳 Docker

The project is designed to run as a multi-container application.

```text
Docker Compose
│
├── Nginx
├── FastAPI
├── PostgreSQL
└── Redis
```

Build:

```bash
docker compose build
```

Start:

```bash
docker compose up -d
```

Check containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

Stop:

```bash
docker compose down
```

Run migrations:

```bash
docker compose run --rm api alembic upgrade head
```

> Avoid `docker compose down -v` unless you intentionally want to remove the database volumes.

---

# 🔑 Authentication Example

Register:

```http
POST /auth/register
```

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "StrongPassword123!"
}
```

Login:

```http
POST /auth/login
```

```json
{
  "email": "john@example.com",
  "password": "StrongPassword123!"
}
```

Response:

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

Use the token:

```http
Authorization: Bearer <access_token>
```

---

# 🔒 Security Practices

The project follows several security principles:

* Passwords are hashed using Argon2
* Passwords are never returned in API responses
* JWT secrets are stored in environment variables
* `.env` is excluded from Git
* Protected routes require authentication
* Admin routes require authorization
* Users cannot access other users' private resources
* Product sorting uses an allowlist
* Request data is validated using Pydantic
* Login attempts are rate limited
* PostgreSQL is treated as the source of truth
* Payment amount is calculated from the server-side order
* Idempotency keys are used for payment creation
* Internal errors should not expose sensitive implementation details

---

# 💰 Payment Architecture

Current implementation uses a mock payment provider:

```text
Client
  │
  ▼
Create Order
  │
  ▼
Create Payment
  │
  ▼
Mock Provider
  │
  ▼
Verify Payment
  │
  ▼
Order Confirmation
```

The payment layer is intentionally separated from order management so that a real provider can be integrated later.

Potential future integrations include:

```text
Stripe
Razorpay
PayPal
```

---

# 📈 Development Roadmap

The project is being built incrementally.

```text
Phase 1   ✅ FastAPI Foundation
Phase 2   ✅ PostgreSQL + SQLAlchemy
Phase 3   ✅ User CRUD
Phase 4   ✅ Authentication + JWT
Phase 5   ✅ Authorization + Roles
Phase 6   ✅ Products + Categories
Phase 7   ✅ Search + Filtering + Pagination
Phase 8   ✅ Cart
Phase 9   ✅ Orders + Checkout
Phase 10  ✅ Addresses + Reviews
Phase 11  ✅ Inventory + Admin
Phase 12  ✅ Payments
Phase 13  🚧 Redis + Background Tasks + Performance
Phase 14  ⏳ Testing + Security + API Hardening
Phase 15  ⏳ Docker + Production Deployment
```

---

# 🔮 Future Improvements

Planned improvements include:

* Production payment gateway
* Payment webhooks
* Better inventory reservation
* Automated email provider integration
* Advanced order/payment reconciliation
* Comprehensive integration testing
* CI/CD with GitHub Actions
* Docker production optimization
* Nginx HTTPS configuration
* Cloud deployment
* Monitoring and logging
* API versioning
* Advanced search
* Object storage for product images
* Refresh tokens
* More granular permissions

---

# 🎯 Learning Goals

This project is not just about creating CRUD APIs.

The goal is to understand how backend systems evolve from:

```text
Simple CRUD
    ↓
Authentication
    ↓
Authorization
    ↓
Business Logic
    ↓
Transactions
    ↓
Payments
    ↓
Caching
    ↓
Performance
    ↓
Testing
    ↓
Security
    ↓
Docker
    ↓
Production Deployment
```

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/your-feature
```

3. Commit your changes

```bash
git commit -m "Add your feature"
```

4. Push the branch

```bash
git push origin feature/your-feature
```

5. Open a Pull Request

---




# 📄 License

This project is currently intended for **learning, experimentation, and portfolio purposes**.

Add a specific open-source license here if/when one is chosen.

---

# 👨‍💻 Author

**Arun Jawlia**

Full Stack Developer | Python Backend | GenAI

GitHub: Add your GitHub profile here

Portfolio: Add your portfolio here

---

## ⭐ If you find this project useful

Give the repository a ⭐ and feel free to explore the code, raise issues, or suggest improvements.
