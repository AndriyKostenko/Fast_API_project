from sqlalchemy.orm import Session

from app.models.user_models import User
from app.models.schemas import CreateUser
from app.security import get_hashed_password


def create_user(db: Session, user: CreateUser):
    db_user = User(id=user.id, name=user.name, surname=user.surname, age=user.age, email=user.email,
                   hashed_password=get_hashed_password(user.hashed_password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user_(db: Session, user_email: str):
    user_ = db.query(User).filter(User.email == user_email).first()
    db.delete(user_)
    db.commit()
    return db.query(User).all()


def get_user_(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_name(db: Session, user_name: str):
    return db.query(User).filter(User.name == user_name).first()


def get_user_by_email(db: Session, user_email: str):
    return db.query(User).filter(User.email == user_email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()




