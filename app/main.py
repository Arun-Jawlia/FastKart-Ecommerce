from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.config import settings
from app.database.init_db import create_tables
from app.database.database import get_db
from app.routers.users import router as users_router
from app.routers.auth import router as auth_router
from app.routers.category import router as category_router
from app.routers.products import router as products_router

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

@app.on_event('startup')
def startup():
    create_tables()


app.include_router(users_router)
app.include_router(auth_router)
app.include_router(category_router)
app.include_router(products_router)

@app.get('/')
def root():
    return {
        "message":"FastKart E-Commerce API is Running"
    }

@app.get("/health")
def health_check():
    return {
        'status':"Healty"
    }

@app.get('/health/db')
def database_health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {
        'database':'Connected'
    }
