from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.init_db import create_tables
from app.database.database import get_db
from app.routers.users import router as users_router
from app.routers.auth import router as auth_router
from app.routers.category import router as category_router
from app.routers.products import router as products_router
from app.routers.cart import router as cart_router
from app.routers.orders import router as orders_router
from app.routers.addresses import router as addresses_router
from app.routers.reviews import router as reviews_router
from app.routers.inventory import router as inventory_router
from app.routers.payments import router as payments_router
from app.database.redis import redis_client

# app = FastAPI(
#     title='FastKar Ecommerce API',
#     description='E-commerce backend built with FastAPI and Postgresql',
#     version='1.0.0'
# )
app = FastAPI(
    title= settings.app_name,
    description = settings.app_description,
    version= settings.app_version
)

# @app.on_event('startup')
# def startup():
#     create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(category_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(addresses_router)
app.include_router(reviews_router)
app.include_router(inventory_router)
app.include_router(payments_router)


@app.get('/')
def root():
    return {
        "message":"FastKart E-Commerce API is Running"
    }

@app.get("/health")
def health_check():
    return {
        'status':"healthy"
    }

@app.get('/health/db')
def database_health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {
        'database':'Connected'
    }

@app.get('/health/redis')
def redis_health_check():
    redis_client.ping()

    return {
        'redis':'Connected'
    }
