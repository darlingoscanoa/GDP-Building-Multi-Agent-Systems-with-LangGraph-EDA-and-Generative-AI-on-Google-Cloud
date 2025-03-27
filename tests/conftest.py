import pytest
import os
from flask import Flask
from portal.app import app as portal_app
from planner.app import app as planner_app

@pytest.fixture
def portal_client():
    """Create a test client for the portal application."""
    portal_app.config['TESTING'] = True
    with portal_app.test_client() as client:
        yield client

@pytest.fixture
def planner_client():
    """Create a test client for the planner application."""
    planner_app.config['TESTING'] = True
    with planner_app.test_client() as client:
        yield client

@pytest.fixture
def mock_gcp_credentials(monkeypatch):
    """Mock Google Cloud credentials for testing."""
    monkeypatch.setenv('GOOGLE_CLOUD_PROJECT', 'test-project')
    monkeypatch.setenv('GOOGLE_APPLICATION_CREDENTIALS', 'test-credentials.json')

@pytest.fixture
def mock_storage_client(mocker):
    """Mock Google Cloud Storage client."""
    mock_client = mocker.patch('google.cloud.storage.Client')
    return mock_client

@pytest.fixture
def mock_vertex_ai(mocker):
    """Mock Google Cloud Vertex AI client."""
    mock_client = mocker.patch('google.cloud.aiplatform.gapic.PredictionServiceClient')
    return mock_client

@pytest.fixture
def test_quiz_data():
    """Sample quiz data for testing."""
    return [
        {
            "question": "What is the capital of France?",
            "options": ["London", "Paris", "Berlin", "Madrid"],
            "answer": "Paris",
            "difficulty": "easy"
        }
    ]

@pytest.fixture
def test_teaching_plan():
    """Sample teaching plan data for testing."""
    return {
        "plan_id": "test-plan-1",
        "content": "Test teaching plan content",
        "schedule": [
            {
                "week": 1,
                "topics": ["Topic 1", "Topic 2"],
                "assignments": ["Assignment 1"]
            }
        ]
    }

@pytest.fixture
def test_course_data():
    """Sample course data for testing."""
    return {
        "course_id": "test-course-1",
        "title": "Test Course",
        "description": "Test course description",
        "materials": [
            {
                "type": "lecture",
                "content": "Test lecture content",
                "week": 1
            }
        ]
    }

@pytest.fixture
def test_assignment_data():
    """Sample assignment data for testing."""
    return {
        "assignment_id": "test-assignment-1",
        "title": "Test Assignment",
        "description": "Test assignment description",
        "due_date": "2024-12-31",
        "course_id": "test-course-1"
    }

@pytest.fixture
def test_book_recommendations():
    """Sample book recommendations for testing."""
    return {
        "recommendations": [
            {
                "book_id": "test-book-1",
                "title": "Test Book",
                "author": "Test Author",
                "description": "Test book description",
                "reading_level": "intermediate",
                "relevance_score": 0.85
            }
        ]
    } 