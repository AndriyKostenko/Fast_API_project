from sqlalchemy.orm import Session

from app.models.models import User
from app.models.schemas import UserSignUp
from app.security.security import get_hashed_password


def create_user(db: Session, user: UserSignUp):
    db_user = User(name=user.name, surname=user.surname, age=user.age, email=user.email,
                   hashed_password=get_hashed_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user_(db: Session, user_email: str):
    user_ = db.query(User).filter(User.email == user_email).first()
    db.delete(user_)
    db.commit()
    return db.query(User).all()


def get_user_by_email(db: Session, user_email: str):
    user = db.query(User).filter(User.email == user_email).first()
    return user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()






























