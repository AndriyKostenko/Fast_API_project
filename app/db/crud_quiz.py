from sqlalchemy.orm import Session

from app.models.models import Quiz, Question, Answer
from app.models.schemas import QuizInfo, QuestionInfo, AnswerInfo


async def create_quiz(db: Session, quiz: QuizInfo):
    db_quiz = Quiz(title=quiz.title,
                   description=quiz.description,
                   total_questions=quiz.total_questions)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz


async def delete_quiz_(db: Session, quiz_title: str):
    quiz = db.query(Quiz).filter(Quiz.title == quiz_title).first()
    db.delete(quiz)
    db.commit()
    return db.query(Quiz).all()


async def get_quiz_by_title(db: Session, quiz_title: str):
    quiz = db.query(Quiz).filter(Quiz.title == quiz_title).first()
    return quiz


async def get_quiz_by_id(db: Session, quiz_id: int):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    return quiz


async def get_quizzes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Quiz).offset(skip).limit(limit).all()


# =============================CREATING OF QUESTIONS===================================

async def create_question(db: Session, question: QuestionInfo):
    db_question = Question(id=question.id, question=question.question, owner_title=question.owner_title)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


async def get_question(db: Session, question: str):
    question = db.query(Question).filter(Question.question == question).first()
    return question


async def delete_question(db: Session, question: str):
    question = db.query(Question).filter(Question.question == question).first()
    db.delete(question)
    db.commit()
    return db.query(Question).all()


async def get_questions_info(db: Session, quiz_title: str):
    return db.query(Question).filter(Question.owner_title == quiz_title).all()


async def get_only_questions_by_quiz_title(db: Session, quiz_title: str):
    return db.query(Question.question).filter(Question.owner_title == quiz_title).all()


# =============================CREATING OF ANSWERS===================================


async def create_answer(db: Session, answer: AnswerInfo):
    db_answer = Answer(id=answer.id,
                       answers=answer.answers,
                       correct_answer=answer.correct_answer,
                       owner_id=answer.owner_id)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


async def get_answer(db: Session, answer: str):
    answer = db.query(Answer).filter(Answer.answers == answer).first()
    return answer


async def delete_answer(db: Session, answers: str):
    answers = db.query(Answer).filter(Answer.answers == answers).first()
    db.delete(answers)
    db.commit()
    return db.query(Answer).all()


async def get_answers_info(db: Session, question_id: int):
    return db.query(Answer).filter(Answer.owner_id == question_id).all()


async def get_answers(db: Session, question_id: int):
    return db.query(Answer.answers).filter(Answer.owner_id == question_id).all()


async def get_correct_answers(db: Session, question_id: int):
    return db.query(Answer.correct_answer).filter(Answer.owner_id == question_id).all()
