import pytest

from app.db.crud_quiz import create_quiz, create_question, create_answer, get_quizzes, delete_quiz_, delete_answer, \
    delete_question, get_answers, get_only_questions_by_quiz_title
from app.models.schemas import QuizInfo, QuestionInfo, AnswerInfo


@pytest.mark.asyncio
async def test_create_quiz_success(session):
    new_quiz = {
        "title": "test_quiz",
        "description": "about_test_quiz",
        "total_questions": 2
    }
    create_quiz_ = await create_quiz(db=session, quiz=QuizInfo(**new_quiz))
    assert create_quiz_.title == 'test_quiz'


@pytest.mark.asyncio
async def test_all_quizzes_success(session):
    quizzes = await get_quizzes(db=session)
    assert len(quizzes) == 1


@pytest.mark.asyncio
async def test_add_questions_success(session):
    new_question = {
        "id": 3,
        "question": 'How old a u?',
        "owner_title": 'test_quiz'
    }
    create_question_ = await create_question(db=session, question=QuestionInfo(**new_question))
    assert create_question_.id == 3


@pytest.mark.asyncio
async def test_add_answers_success(session):
    new_answer = {
        "id": 3,
        "answers": 'good, bad, not bad',
        "correct_answer": 'good',
        "owner_id": 3
    }
    create_answer_ = await create_answer(db=session, answer=AnswerInfo(**new_answer))
    assert create_answer_.correct_answer == 'good'


@pytest.mark.asyncio
async def test_delete_answers(session):
    await delete_answer(db=session, answers='good, bad, not bad')
    answers = await get_answers(db=session, question_id=3)
    assert len(answers) == 0


@pytest.mark.asyncio
async def test_delete_questions(session):
    await delete_question(db=session, question='How old a u?')
    questions = await get_only_questions_by_quiz_title(db=session, quiz_title="test_quiz")
    assert len(questions) == 0


@pytest.mark.asyncio
async def test_delete_quiz_success(session):
    await delete_quiz_(db=session, quiz_title='test_quiz')
    quizzes = await get_quizzes(db=session)
    assert len(quizzes) == 0



