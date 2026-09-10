from app.database.base import Base
from app.database.database import engine

from app.models.user import User

def create_tables():
    Base.metadata.create_all(bind = engine)