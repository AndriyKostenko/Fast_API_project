async def test_create_quiz(client):
    response = client.post("/add_quiz", json={'id': 1,
                                                    'title': 'test_quiz',
                                                    'description': 'about_test_quiz',
                                                    'total_questions': 2,
                                                    'quiz_score': 0,
                                                    'owner_email': 'test@mail.com'})
    assert response.status_code == 201


async def test_all_quizzes(client):
    response = await client.get("/quizzes/")
    assert response.json()[0] == {'id': 1,
                                  'title': 'test_quiz',
                                  'description': 'about_test_quiz',
                                  'total_questions': 2,
                                  'quiz_score': 0,
                                  'owner_email': 'test@mail.com'}
    assert response.status_code == 200
