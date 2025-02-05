from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class UserToken(db.Model):
    token = db.Column(db.String(36), primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'token': self.token,
            'user_name': self.user_name,
            'created_at': self.created_at.isoformat()
        }

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(500), nullable=False)
    responses = db.Column(db.JSON, nullable=False)
    order_index = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "Question": self.question_text,
            "Responses": self.responses
        }

class SurveyResponse(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    question_index = db.Column(db.Integer, nullable=False)
    response = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'question_index': self.question_index,
            'response': self.response,
            'created_at': self.created_at.isoformat()
        }

def get_user_from_token(token):
    user_token = UserToken.query.filter_by(token=token).first()
    if not user_token:
        return None
    return user_token.user_name

def init_db():
    print("Starting database initialization...")
    with app.app_context():
        db.create_all()
        print("Database tables created.")
        
        # Only initialize if no questions exist
        if Question.query.count() == 0:
            print("No questions found. Loading from survey_questions.json...")
            with open('survey_questions.json', 'r') as f:
                questions = json.load(f)
                for idx, q in enumerate(questions):
                    question = Question(
                        question_text=q['Question'],
                        responses=q['Responses'],
                        order_index=idx
                    )
                    db.session.add(question)
            db.session.commit()
            print(f"Loaded {len(questions)} questions into database.")
        else:
            print(f"Found {Question.query.count()} existing questions. Skipping initialization.")

@app.route('/')
def root():
    return jsonify({
        "status": "online",
        "version": "1.0.0",
        "endpoints": [
            "/api/health",
            "/api/get_auth_token",
            "/api/questions/<token>",
            "/api/responses/<token>",
            "/api/responses/<token>/<user_name>",
            "/api/progress/<token>"
        ]
    })

@app.route('/api/get_auth_token', methods=['POST'])
def get_auth_token():
    data = request.json
    if not data or 'user_name' not in data:
        return jsonify({'error': 'user_name is required'}), 400
    
    # Generate a new token
    token = str(uuid.uuid4())
    user_token = UserToken(token=token, user_name=data['user_name'])
    db.session.add(user_token)
    db.session.commit()
    
    return jsonify({'token': token, 'user_name': data['user_name']}), 201

@app.route('/api/questions/<token>', methods=['GET'])
def get_questions(token):
    user_name = get_user_from_token(token)
    if not user_name:
        return jsonify({'error': 'Invalid token'}), 401
        
    questions = Question.query.order_by(Question.order_index).all()
    return jsonify([q.to_dict() for q in questions])

@app.route('/api/responses/<token>', methods=['POST'])
def save_response(token):
    user_name = get_user_from_token(token)
    if not user_name:
        return jsonify({'error': 'Invalid token'}), 401
        
    data = request.json
    if not all(k in data for k in ['question_index', 'response']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    response = SurveyResponse(
        id=str(uuid.uuid4()),
        user_name=user_name,
        question_index=data['question_index'],
        response=data['response']
    )
    db.session.add(response)
    db.session.commit()
    
    return jsonify(response.to_dict()), 201

@app.route('/api/responses/<token>/<user_name>', methods=['GET'])
def get_responses(token, user_name):
    token_user = get_user_from_token(token)
    if not token_user:
        return jsonify({'error': 'Invalid token'}), 401
        
    responses = SurveyResponse.query.filter_by(user_name=user_name).all()
    return jsonify([r.to_dict() for r in responses])

@app.route('/api/progress/<token>', methods=['GET'])
def get_progress(token):
    user_name = get_user_from_token(token)
    if not user_name:
        return jsonify({'error': 'Invalid token'}), 401
        
    total_questions = Question.query.count()
    answered_questions = SurveyResponse.query.filter_by(user_name=user_name).count()
    
    return jsonify({
        'total_questions': total_questions,
        'answered_questions': answered_questions,
        'progress': (answered_questions / total_questions) if total_questions > 0 else 0
    })

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
else:
    init_db()
