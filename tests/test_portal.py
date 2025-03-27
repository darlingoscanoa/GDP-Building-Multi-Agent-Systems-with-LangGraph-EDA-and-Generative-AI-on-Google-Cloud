import pytest
from portal.app import app
from portal.quiz import generate_quiz_question
from portal.answer import answer_thinking

def test_home_page(portal_client):
    """Test that the home page loads successfully."""
    response = portal_client.get('/')
    assert response.status_code == 200
    assert b'AiDemy' in response.data

def test_quiz_page(portal_client):
    """Test that the quiz page loads successfully."""
    response = portal_client.get('/quiz')
    assert response.status_code == 200
    assert b'Quiz' in response.data

def test_courses_page(portal_client):
    """Test that the courses page loads successfully."""
    response = portal_client.get('/courses')
    assert response.status_code == 200
    assert b'Courses' in response.data

def test_assignment_page(portal_client):
    """Test that the assignment page loads successfully."""
    response = portal_client.get('/assignment')
    assert response.status_code == 200
    assert b'Assignment' in response.data

def test_generate_quiz(portal_client, mock_vertex_ai):
    """Test quiz generation endpoint."""
    response = portal_client.get('/generate_quiz')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'question' in data[0]
    assert 'options' in data[0]
    assert 'answer' in data[0]

def test_check_answers(portal_client, test_quiz_data):
    """Test answer checking endpoint."""
    test_data = {
        'quiz': test_quiz_data,
        'answers': ['Paris']
    }
    response = portal_client.post('/check_answers', json=test_data)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['is_correct'] == True

def test_download_course_audio(portal_client, mock_storage_client):
    """Test course audio download endpoint."""
    response = portal_client.get('/download_course_audio/1')
    assert response.status_code == 200
    assert response.mimetype == 'audio/wav'

def test_generate_quiz_question(mock_vertex_ai):
    """Test quiz question generation function."""
    question = generate_quiz_question("teaching_plan.txt", "easy", "test-region")
    assert isinstance(question, dict)
    assert 'question' in question
    assert 'options' in question
    assert 'answer' in question
    assert 'difficulty' in question

def test_answer_thinking(mock_vertex_ai):
    """Test answer thinking function."""
    reasoning = answer_thinking(
        "What is the capital of France?",
        ["London", "Paris", "Berlin", "Madrid"],
        "London",
        "Paris",
        "test-region"
    )
    assert isinstance(reasoning, str)
    assert len(reasoning) > 0

def test_error_handling(portal_client):
    """Test error handling for invalid requests."""
    # Test invalid quiz submission
    response = portal_client.post('/check_answers', json={})
    assert response.status_code == 400
    
    # Test invalid audio download
    response = portal_client.get('/download_course_audio/invalid')
    assert response.status_code == 404

def test_rate_limiting(portal_client):
    """Test rate limiting functionality."""
    # Make multiple requests in quick succession
    for _ in range(10):
        response = portal_client.get('/generate_quiz')
        assert response.status_code == 200
    
    # Check rate limit headers
    assert 'X-RateLimit-Limit' in response.headers
    assert 'X-RateLimit-Remaining' in response.headers
    assert 'X-RateLimit-Reset' in response.headers 