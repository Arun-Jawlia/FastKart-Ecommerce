from fastapi import FastAPI
from app.core.config import settings

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