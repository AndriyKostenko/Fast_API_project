from sqlalchemy.orm import Session

from app.models.models import User
from app.models.schemas import UserSignUp
from app.security.security import get_hashed_password


async def create_user(db: Session, user: UserSignUp):
    db_user = User(name=user.name, surname=user.surname, age=user.age, email=user.email,
                   hashed_password=get_hashed_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def delete_user_(db: Session, user_email: str):
    user_ = db.query(User).filter(User.email == user_email).first()
    db.delete(user_)
    db.commit()
    return db.query(User).all()


async def get_user_by_email(db: Session, user_email: str):
    user = db.query(User).filter(User.email == user_email).first()
    return user


async def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


async def update_last_quiz_score(db: Session, user_email: str, user_points: int):
    db.query(User).filter(User.email == user_email).update({'last_quiz_score': user_points})
    db.commit()
    last_user_points = db.query(User.last_quiz_score).filter(User.email == user_email).first()
    return last_user_points


async def update_last_quiz_done(db: Session, user_email: str, quiz_title: str):
    db.query(User).filter(User.email == user_email).update({'last_quiz_done': quiz_title})
    db.commit()
    last_quiz = db.query(User.last_quiz_done).filter(User.email == user_email).first()
    return last_quiz


async def update_last_quiz_done_date(db: Session, user_email: str, quiz_date: str):
    db.query(User).filter(User.email == user_email).update({'last_quiz_done_date': quiz_date})
    db.commit()
    last_quiz_date = db.query(User.last_quiz_done_date).filter(User.email == user_email).first()
    return last_quiz_date
































