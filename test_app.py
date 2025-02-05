import pytest
import json
from app import app, db, Question, UserToken, SurveyResponse

@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create test questions
            question = Question(
                question_text="Test Question",
                responses=["Option 1", "Option 2"],
                order_index=0
            )
            db.session.add(question)
            db.session.commit()
        yield client
        
        with app.app_context():
            db.drop_all()

def test_get_auth_token(client):
    # Test getting a token
    response = client.post('/api/get_auth_token',
                          json={'user_name': 'testuser'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'token' in data
    assert data['user_name'] == 'testuser'
    
    # Test missing username
    response = client.post('/api/get_auth_token', json={})
    assert response.status_code == 400

def test_get_questions_with_token(client):
    # First get a token
    auth_response = client.post('/api/get_auth_token',
                              json={'user_name': 'testuser'})
    token = json.loads(auth_response.data)['token']
    
    # Test getting questions with valid token
    response = client.get(f'/api/questions/{token}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['Question'] == "Test Question"
    
    # Test invalid token
    response = client.get('/api/questions/invalid-token')
    assert response.status_code == 401

def test_save_response_with_token(client):
    # Get a token
    auth_response = client.post('/api/get_auth_token',
                              json={'user_name': 'testuser'})
    token = json.loads(auth_response.data)['token']
    
    # Test saving response with valid token
    response = client.post(
        f'/api/responses/{token}',
        json={
            'question_index': 0,
            'response': 'Option 1'
        }
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['user_name'] == 'testuser'
    assert data['response'] == 'Option 1'
    
    # Test invalid token
    response = client.post(
        '/api/responses/invalid-token',
        json={
            'question_index': 0,
            'response': 'Option 1'
        }
    )
    assert response.status_code == 401
    
    # Test missing required fields
    response = client.post(
        f'/api/responses/{token}',
        json={}
    )
    assert response.status_code == 400

def test_get_responses_with_token(client):
    # Get a token and save a response first
    auth_response = client.post('/api/get_auth_token',
                              json={'user_name': 'testuser'})
    token = json.loads(auth_response.data)['token']
    
    client.post(
        f'/api/responses/{token}',
        json={
            'question_index': 0,
            'response': 'Option 1'
        }
    )
    
    # Test getting responses with valid token
    response = client.get(f'/api/responses/{token}/testuser')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['user_name'] == 'testuser'
    assert data[0]['response'] == 'Option 1'
    
    # Test invalid token
    response = client.get('/api/responses/invalid-token/testuser')
    assert response.status_code == 401

def test_get_progress_with_token(client):
    # Get a token and save a response first
    auth_response = client.post('/api/get_auth_token',
                              json={'user_name': 'testuser'})
    token = json.loads(auth_response.data)['token']
    
    client.post(
        f'/api/responses/{token}',
        json={
            'question_index': 0,
            'response': 'Option 1'
        }
    )
    
    # Test getting progress with valid token
    response = client.get(f'/api/progress/{token}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['total_questions'] == 1
    assert data['answered_questions'] == 1
    assert data['progress'] == 1.0
    
    # Test invalid token
    response = client.get('/api/progress/invalid-token')
    assert response.status_code == 401
