from typing import List
from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from app.db.crud_quiz import get_quiz_by_title, get_quizzes, delete_quiz, create_quiz, create_question, get_question, \
    get_answer, create_answer, get_questions, get_answers, get_quiz_by_id, get_correct_answers, update_quiz_score, \
    get_questions_info, get_answers_info
from app.db.database import get_db
from app.security.deps import get_current_user
from app.models.schemas import QuizInfo, QuestionInfo, AnswerInfo, Answer, Question


route = APIRouter(tags=['quiz'])


@route.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')


@route.post("/add_quiz", summary="Create new quiz")
async def add_quiz(quiz: QuizInfo = Depends(QuizInfo), db: Session = Depends(get_db)):
    db_quiz = get_quiz_by_title(db, quiz_title=quiz.title)
    if db_quiz:
        raise HTTPException(status_code=400, detail="Such quiz already registered!")
    return create_quiz(db=db, quiz=quiz)


@route.post("/add_questions", summary="Create new questions")
async def add_question(question: QuestionInfo = Depends(QuestionInfo), db: Session = Depends(get_db)):
    db_question = get_question(db, question=question.question)
    if db_question:
        raise HTTPException(status_code=400, detail="Such question already registered!")
    return create_question(db=db, question=question)


@route.post("/add_answers", summary="Create new answers")
async def add_answers(answer: AnswerInfo = Depends(AnswerInfo), db: Session = Depends(get_db)):
    db_answer = get_answer(db, answer=answer.answers)
    if db_answer:
        raise HTTPException(status_code=400, detail="Such answer already registered!")
    return create_answer(db=db, answer=answer)


@route.get("/quizzes/", summary='Details of all quizzes for specific user.', response_model=List[QuizInfo])
async def all_quizzes(owner_email: str,
                      current_user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if current_user:
        quizzes = get_quizzes(db, owner_email=owner_email)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"})
    return quizzes


@route.get("/questions/", summary='All questions for the specific quiz.', response_model=List[QuestionInfo])
async def all_questions(quiz_id: int,
                        current_user: dict = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    if current_user:
        questions = get_questions_info(db, quiz_id=quiz_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"})
    return questions


@route.get("/answers/", summary='All answers for the specific question.', response_model=List[AnswerInfo])
async def all_answers(question_id: int,
                      current_user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if current_user:
        answers = get_answers_info(db, question_id=question_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"})
    return answers


@route.get('/quizzes/{quiz_title}', summary='Get quiz by title.', response_model=QuizInfo)
async def get_quiz(quiz_title: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user:
        db_quiz = get_quiz_by_title(db, quiz_title=quiz_title)
        if db_quiz is None:
            raise HTTPException(status_code=404, detail="Quiz not found.")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"})
    return db_quiz


@route.delete("/quizzes/{quiz_title}", summary='Delete quiz by title.', response_model=List[QuizInfo])
async def delete_user(quiz_title: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user:
        db_quiz = await get_quiz_by_title(db, quiz_title=quiz_title)
        if not db_quiz:
            raise HTTPException(status_code=400, detail="Quiz not found.")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"})
    return delete_quiz(db=db, quiz_title=quiz_title)


@route.post("/quizzes/evaluate", summary='Evaluate the selected quiz fro current user.')
async def evaluate_quiz(quiz_id: int,
                        questions: Question = Depends(Question),
                        answers: Answer = Depends(Answer),
                        current_user: dict = Depends(get_current_user),
                        db: Session = Depends(get_db)):  # 1 Quiz, 2 ques. for quiz, 3 variants of answers for quest.

    if current_user:
        db_quiz = get_quiz_by_id(db=db, quiz_id=quiz_id)
        if not db_quiz:
            raise HTTPException(status_code=400, detail="Quiz not found.")

        db_questions = get_questions(db=db, quiz_id=quiz_id)
        db_answer_1 = get_answers(db=db, question_id=questions.question_1_id)
        db_answer_2 = get_answers(db=db, question_id=questions.question_2_id)
        db_correct_answers_1 = get_correct_answers(db=db, question_id=questions.question_1_id)
        db_correct_answers_2 = get_correct_answers(db=db, question_id=questions.question_2_id)
        user_answers = answers
        list_user_answers = [answers.answer_1, answers.answer_2]

        #make a test for IndexError
        list_correct_answers = [db_correct_answers_1[0][0], db_correct_answers_2[0][0]]

        user_points = 0
        for ans in range(len(list_user_answers)):
            if list_user_answers[ans] == list_correct_answers[ans]:
                user_points += 1

        saved_points = update_quiz_score(db=db, quiz_id=quiz_id, user_points=user_points)

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"})

    return {'user': current_user['name'] + ' ' + current_user['surname'],
            'quiz_title': db_quiz.title,
            'db_questions': db_questions,
            'db_answers': [db_answer_1, db_answer_2],
            'db_correct_answers': list_correct_answers,
            'user_answers': user_answers,
            'user_points': saved_points,
            }

