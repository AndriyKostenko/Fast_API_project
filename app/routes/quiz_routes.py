import datetime
from typing import List
from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from time import gmtime, strftime

from app.db.crud_quiz import get_quiz_by_title, get_quizzes, create_quiz, create_question, get_question, \
    get_answer, create_answer, get_answers, get_correct_answers, \
    get_questions_info, get_answers_info, get_only_questions_by_quiz_title, delete_quiz_
from app.db.crud_user import update_last_quiz_score, update_last_quiz_done, update_last_quiz_done_date
from app.db.database import get_db
from app.security.deps import get_current_user
from app.models.schemas import QuizInfo, QuestionInfo, AnswerInfo, Questions, Answers, QuizTitle

route = APIRouter(tags=['quiz'])


@route.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')


@route.post("/add_quiz", summary="Create new quiz")
async def add_quiz(quiz: QuizInfo, db: Session = Depends(get_db)):
    db_quiz = await get_quiz_by_title(db, quiz_title=quiz.title)
    if db_quiz:
        raise HTTPException(status_code=400, detail="Such quiz already registered!")
    return await create_quiz(db=db, quiz=quiz)


@route.post("/add_questions", summary="Create new questions")
async def add_question(question: QuestionInfo, db: Session = Depends(get_db)):
    db_question = await get_question(db, question=question.question)
    if db_question:
        raise HTTPException(status_code=400, detail="Such question already registered!")
    return await create_question(db=db, question=question)


@route.post("/add_answers", summary="Create new answers")
async def add_answers(answer: AnswerInfo, db: Session = Depends(get_db)):
    db_answer = await get_answer(db, answer=answer.answers)
    if db_answer:
        raise HTTPException(status_code=400, detail="Such answer already registered!")
    return await create_answer(db=db, answer=answer)


@route.get("/quizzes/", summary='Details of all quizzes for specific user.', response_model=List[QuizInfo])
async def all_quizzes(current_user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if current_user:
        quizzes = await get_quizzes(db)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"})
    return quizzes


@route.get("/questions/{quiz_title}", summary='All questions for the specific quiz.', response_model=List[QuestionInfo])
async def all_questions(quiz_title: str,
                        current_user: dict = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    if current_user:
        questions = await get_questions_info(db, quiz_title=quiz_title)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"})
    return questions


@route.get("/answers/{question_id}", summary='All answers for the specific question.', response_model=List[AnswerInfo])
async def all_answers(question_id: int,
                      current_user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if current_user:
        answers = await get_answers_info(db, question_id=question_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"})
    return answers


@route.get('/quizzes/{quiz_title}', summary='Get quiz by title.', response_model=QuizInfo)
async def get_quiz(quiz_title: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user:
        db_quiz = await get_quiz_by_title(db, quiz_title=quiz_title)
        if db_quiz is None:
            raise HTTPException(status_code=404, detail="Quiz not found.")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"})
    return db_quiz


@route.delete("/delete_quiz/{quiz_title}", summary='Delete quiz by title.', response_model=List[QuizInfo])
async def delete_quiz(quiz_title: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user:
        db_quiz = await get_quiz_by_title(db, quiz_title=quiz_title)
        if not db_quiz:
            raise HTTPException(status_code=400, detail="Quiz not found.")
        await delete_quiz_(db=db, quiz_title=quiz_title)
        quizzes = await get_quizzes(db)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"})
    return quizzes


@route.post("/quizzes/evaluate/", summary='Evaluate the selected quiz fro current user.')
async def evaluate_quiz(quiz_title: QuizTitle,
                        questions: Questions,
                        answers: Answers,
                        current_user: dict = Depends(get_current_user),
                        db: Session = Depends(get_db)):  # 1 Quiz, 2 ques. for quiz, 3 variants of answers for quest.

    if current_user:
        db_quiz = await get_quiz_by_title(db=db, quiz_title=quiz_title.quiz_title)
        if not db_quiz:
            raise HTTPException(status_code=400, detail="Quiz not found.")

        db_questions = await get_only_questions_by_quiz_title(db=db, quiz_title=quiz_title.quiz_title)
        db_answer_1 = await get_answers(db=db, question_id=questions.question_1_id)
        db_answer_2 = await get_answers(db=db, question_id=questions.question_2_id)
        db_correct_answers_1 = await get_correct_answers(db=db, question_id=questions.question_1_id)
        db_correct_answers_2 = await get_correct_answers(db=db, question_id=questions.question_2_id)

        list_user_answers = [answers.answer_1, answers.answer_2]
        list_correct_answers = [db_correct_answers_1[0][0], db_correct_answers_2[0][0]]

        user_points = 0
        for ans in range(len(list_user_answers)):
            if list_user_answers[ans] == list_correct_answers[ans]:
                user_points += 1

        last_quiz_score = await update_last_quiz_score(db=db,
                                                       user_email=current_user['email'],
                                                       user_points=user_points)
        last_quiz_done = await update_last_quiz_done(db=db,
                                                     user_email=current_user['email'],
                                                     quiz_title=quiz_title.quiz_title)
        last_quiz_done_date = await update_last_quiz_done_date(db=db,
                                                               user_email=current_user['email'],
                                                               quiz_date=str(datetime.datetime.now()))

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"})

    return {'user': current_user['name'] + ' ' + current_user['surname'],
            'Last_quiz_done': last_quiz_done['last_quiz_done'],
            'db_questions': db_questions,
            'db_answers': [db_answer_1, db_answer_2],
            'db_correct_answers': list_correct_answers,
            'user_answers': list_user_answers,
            'last_quiz_score': last_quiz_score['last_quiz_score'],
            'last_quiz_done': last_quiz_done_date['last_quiz_done_date']
            }
