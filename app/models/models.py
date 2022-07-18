from sqlalchemy import ForeignKey, Column, Integer, String, Text
from app.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, index=True)
    name = Column(String, unique=False)
    surname = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, primary_key=True, unique=True, nullable=False)
    hashed_password = Column(String, unique=True, nullable=False)

    quizzes = relationship('Quiz', back_populates='owner')


class Quiz(Base):
    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    total_questions = Column(Integer, nullable=False)
    quiz_score = Column(Integer, nullable=True)
    owner_email = Column(String, ForeignKey('users.email'))

    owner = relationship('User', back_populates='quizzes')

    questions = relationship('Question', back_populates='owner')


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    question = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('quizzes.id'))

    owner = relationship('Quiz', back_populates='questions')

    answers = relationship('Answer', back_populates='owner')


class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    answers = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('questions.id'))

    owner = relationship('Question', back_populates='answers')






