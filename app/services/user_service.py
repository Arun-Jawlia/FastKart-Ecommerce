from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


def create_user(db: Session, user_data: UserCreate) -> User:
    user = User(
        name = user_data.name,
        email = user_data.email,
        password = hash_password(user_data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_user_by_email(db: Session, email: str)-> User | None:
    statement = select(User).where(User.email == email)
    return db.scalar(statement)

def get_user_by_id(db: Session, user_id: int) -> User | None :
    userExist = db.get(User, user_id)
    return userExist

def get_all_users(db: Session) -> list[User]:
    statement = select(User)
    return list(
        db.scalars(statement).all()
    )

def update_user(db:Session, user: User, user_data: UserUpdate) -> User:
    update_data = user_data.model_dump(
        exclude_unset = True
    )
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user
        

def delete_user(db: Session,user: User) -> None:
    db.delete(user)
    db.commit()