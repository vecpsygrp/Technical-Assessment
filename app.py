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
    user_name = db.Column(db.String(100), nullable=False)  # Simple identifier
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
            "/api/questions",
            "/api/responses/<user_name>",
            "/api/progress/<user_name>"
        ]
    })

@app.route('/api/questions', methods=['GET'])
def get_questions():
    questions = Question.query.order_by(Question.order_index).all()
    return jsonify([q.to_dict() for q in questions])

@app.route('/api/responses', methods=['POST'])
def save_response():
    data = request.json
    if not all(k in data for k in ['user_name', 'question_index', 'response']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    response = SurveyResponse(
        id=str(uuid.uuid4()),
        user_name=data['user_name'],
        question_index=data['question_index'],
        response=data['response']
    )
    db.session.add(response)
    db.session.commit()
    
    return jsonify(response.to_dict()), 201

@app.route('/api/responses/<user_name>', methods=['GET'])
def get_responses(user_name):
    responses = SurveyResponse.query.filter_by(user_name=user_name).all()
    return jsonify([r.to_dict() for r in responses])

@app.route('/api/progress/<user_name>', methods=['GET'])
def get_progress(user_name):
    total_questions = Question.query.count()
    responses = SurveyResponse.query.filter_by(user_name=user_name).all()
    completed_questions = len(set(r.question_index for r in responses))
    
    return jsonify({
        'total_questions': total_questions,
        'completed_questions': completed_questions,
        'progress_percentage': (completed_questions / total_questions) * 100 if total_questions > 0 else 0
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "API is running"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
else:
    # Initialize database for production environment
    init_db()
