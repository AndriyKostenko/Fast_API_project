import pytest

from app.db.crud_quiz import create_quiz, create_question, create_answer
from app.models.schemas import QuizInfo, QuestionInfo, AnswerInfo


@pytest.mark.asyncio
async def test_create_quiz_success(db):
    new_quiz = {
        "id": 1,
        "title": "test_quiz",
        "description": "about_test_quiz",
        "total_questions": 2,
        "quiz_score": 0,
        "owner_email": "test@mail.com"}
    create_quiz_ = await create_quiz(db=db, quiz=QuizInfo(**new_quiz))
    assert create_quiz_.title == 'test_quiz'




@pytest.mark.asyncio
async def test_create_quiz_not_success(db):
    new_quiz = {
        "id": 1,
        "title": "test_quiz",
        "description": "about_test_quiz",
        "total_questions": 2,
        "quiz_score": 0,
        "owner_email": "test@mail.com"}
    create_quiz_ = await create_quiz(db=db, quiz=QuizInfo(**new_quiz))
    assert create_quiz_.title != 'test_quiz'


@pytest.mark.asyncio
async def test_add_questions_success(db):
    new_questions = {
        "id": 1,
        "question": 'How old a u?',
        "owner_id": 1
    }
    create_question_ = await create_question(db=db, question=QuestionInfo(**new_questions))
    assert create_question_.owner_id == 1


@pytest.mark.asyncio
async def test_add_questions_not_success(db):
    new_questions = {
        "id": 1,
        "question": 'How old a u?',
        "owner_id": 1
    }
    create_question_ = await create_question(db=db, question=QuestionInfo(**new_questions))
    assert create_question_.owner_id != 1


@pytest.mark.asyncio
async def test_add_answer_success(db):
    new_answer = {
        "id": 1,
        "answers": ['I\'m fine.', 'I\'m not fine', 'OK'],
        "correct_answer": 'OK',
        "owner_id": 1
    }
    create_answer_ = await create_answer(db=db, answer=AnswerInfo(**new_answer))
    assert create_answer_.correct_answer == 'OK'


