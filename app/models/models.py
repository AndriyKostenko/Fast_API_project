from sqlalchemy import Sequence, ForeignKey, Column, Integer, String, Text, DateTime
from app.db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Sequence


class User(Base):
    __tablename__ = 'users'

    seq = Sequence('users_id_seq', start=1)

    id = Column('id', Integer, seq,  server_default=seq.next_value())
    name = Column(String, unique=False)
    surname = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, primary_key=True, unique=True, nullable=False)
    hashed_password = Column(String, unique=True, nullable=False)
    last_quiz_done = Column(String, nullable=True)
    last_quiz_score = Column(Integer, nullable=True)
    last_quiz_done_date = Column(DateTime, nullable=True)


class Quiz(Base):
    __tablename__ = 'quizzes'

    seq = Sequence('quizzes_id_seq', start=1)

    id = Column('id', Integer, seq, server_default=seq.next_value(), primary_key=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    total_questions = Column(Integer, nullable=False)

    questions = relationship('Question', back_populates='owner')


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    question = Column(String, nullable=False)
    owner_title = Column(String, ForeignKey('quizzes.title'))

    owner = relationship('Quiz', back_populates='questions')

    answers = relationship('Answer', back_populates='owner')


class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    answers = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('questions.id'))

    owner = relationship('Question', back_populates='answers')






