from app import app, db, Survey
import json

def init_survey_questions():
    with app.app_context():
        # Clear existing surveys
        Survey.query.delete()
        db.session.commit()

        # Load questions from JSON
        with open('survey_questions.json', 'r') as f:
            questions = json.load(f)

        # Add questions to database
        for question_data in questions:
            question = Survey(
                question=question_data['Question'],
                answers=json.dumps(question_data['Responses'])
            )
            db.session.add(question)

        db.session.commit()
        print("Survey questions initialized successfully!")

if __name__ == '__main__':
    init_survey_questions()
