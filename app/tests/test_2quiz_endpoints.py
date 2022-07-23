import pytest


@pytest.mark.asyncio
async def test_create_quiz(client):
    async with client as cl:
        response = await cl.post("/add_quiz", json={"title": "Sport",
                                                    "description": "about sport",
                                                    "total_questions": 2
                                                    })
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_quiz_already_exist(client):
    async with client as cl:
        response = await cl.post("/add_quiz", json={"title": "Sport",
                                                    "description": "about sport",
                                                    "total_questions": 2
                                                    })
    assert response.json().get("detail") == "Such quiz already registered!"
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_question_1(client):
    async with client as cl:
        response = await cl.post("/add_questions", json={"id": 1,
                                                         "question": "The best NBA player?",
                                                         "owner_title": "Sport"
                                                         })
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_question_2(client):
    async with client as cl:
        response = await cl.post("/add_questions", json={"id": 2,
                                                         "question": "The worst NBA player?",
                                                         "owner_title": "Sport"
                                                         })
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_answers_1(client):
    async with client as cl:
        response = await cl.post("/add_answers", json={"id": 1,
                                                       "answers": "Jordan, Leo, Michael",
                                                       "correct_answer": "Jordan",
                                                       "owner_id": 1
                                                       })
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_answers_2(client):
    async with client as cl:
        response = await cl.post("/add_answers", json={"id": 2,
                                                       "answers": "Bob, Hob, Don",
                                                       "correct_answer": "Leo",
                                                       "owner_id": 2
                                                       })
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_list_quizzes_for_unauthorized(client):
    async with client as cl:
        response = await cl.get("/quizzes/")
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.asyncio
async def test_get_quizzes(auth_client):
    async with auth_client as cl:
        response = await cl.get("/quizzes/")

    assert response.json()[0] == {"title": "Sport",
                                  "description": "about sport",
                                  "total_questions": 2
                                  }
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_questions(auth_client):
    async with auth_client as cl:
        response = await cl.get("/questions/Sport")
    assert response.json()[0] == {"id": 1,
                                  "question": "The best NBA player?",
                                  "owner_title": "Sport"
                                  }
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_answers(auth_client):
    async with auth_client as cl:
        response = await cl.get("/answers/1")
    assert response.json()[0] == {"id": 1,
                                  "answers": "Jordan, Leo, Michael",
                                  "correct_answer": "Jordan",
                                  "owner_id": 1
                                  }
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_quiz(auth_client):
    async with auth_client as cl:
        response = await cl.get('/quizzes/Sport')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_evaluate_quiz(auth_client):
    async with auth_client as cl:
        response = await cl.post("/quizzes/evaluate/", json={"quiz_title": {
            "quiz_title":
                "Sport"},
            "questions": {
                "question_1_id": 1,
                "question_2_id": 2
            },
            "answers": {
                "answer_1": "mike",
                "answer_2": "spike"
            }
        })
        assert response.json()['last_quiz_score'] == 0
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_quiz(auth_client):
    async with auth_client as cl:
        response = await cl.delete("/delete_quiz/Sport")
    assert response.status_code == 200


# deleting created user at the end for preventing authorization errors during tests.
@pytest.mark.asyncio
async def test_delete_user(auth_client):
    async with auth_client as cl:
        response = await cl.delete("/delete_user/test@mail.com")
    assert response.status_code == 200
