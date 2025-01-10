# Mobile Developer Technical Assignment

## Overview
Build a React Native quiz application that demonstrates your ability to implement state management, local storage, and UI development following mobile best practices.

## API Server Setup
This repository includes a simple Flask API server that provides the quiz questions. Python is required to run the server. Once you have Python installed and in your PATH, you can follow these steps to run it:

1. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the API server:
```bash
python app.py
```

Alternatively, if you prefer to keep things simple, you can use the static question data directly from `survey_questions.json` in your React Native app. However, we recommend using the Flask API as it provides a more realistic development experience with proper data persistence and state management.

The API will be available at `http://localhost:5000` with the following endpoints:
- `GET /api/questions` - Returns the list of quiz questions
- `POST /api/responses` - Save an answer
  ```json
  {
    "user_name": "john_doe",  
    "question_index": 0,      
    "response": "Without any difficulty" 
  }
  ``` 
  
- `GET /api/responses/<user_name>` - Get all responses for a user
- `GET /api/progress/<user_name>` - Get survey progress for a user
- `GET /api/health` - Health check endpoint

### API Response Examples

#### Get Progress Response
```json
{
  "total_questions": 10,
  "completed_questions": 3,
  "progress_percentage": 30.0
}
```

#### Get Responses
```json
[
  {
    "id": "uuid",
    "user_name": "john_doe",
    "question_index": 0,
    "response": "Without any difficulty",
    "created_at": "2025-01-06T20:03:36.789Z"
  }
]
```

### Note
The server uses SQLite for data storage. A new database will be created automatically when you first run the app. If you want to reset all data, stop the flask server and delete the `survey.db` file.

## Your Task: React Native Quiz App

### Core Features

1. Create a React Native app that implements a step-by-step health survey:
   - Display one question per screen
   - Show multiple-choice answers for the current question
   - Include Next/Previous navigation buttons
   - Prevent proceeding without selecting an answer

2. Implement the following screens:
   - Welcome/Start screen
   - Question screen (one question at a time)
   - Progress indicator showing current question number (e.g., "Question 3/10")
   - Final completion report showing all responses

3. Integrate with the Flask API to:
   - Fetch survey questions
   - Save responses after each question
   - Track and persist survey progress

   
### Technical Requirements
- Use React Native (latest stable version)
- Implement React hooks (useState, useEffect) for state management
- Use AsyncStorage for local persistence (saving current question and responses)
- Demonstrate proper data fetching patterns (loading states, error handling)
- Follow React Native best practices for component structure

### UI/UX Requirements
- Clean, intuitive interface for each question screen
- Clear visual hierarchy for question text and answer options
- Smooth transitions between questions
- Visible progress indicator (e.g., "3/10")
- Disabled "Next" button until an answer is selected
- Clear completion summary showing all questions and selected answers

### Data Structure
The API provides questions in the following format:
```json
{
  "Question": "Are you able to walk up a hill without stopping?",
  "Responses": [
    "Without any difficulty",
    "With a little difficulty",
    "With some difficulty",
    "With much difficulty",
    "Unable to do"
  ]
}
```

### Bonus Points (Completely Optional)
- Enhanced Features:
  - Ability to review and modify previous answers
  - Save partial progress and resume later
  - Offline support with data sync
  - Custom Flask API extensions
- Polish:
  - Screen transition animations
  - Creative results visualization
  - Performance optimizations
- Code Quality:
  - Unit tests
  - Code documentation

## Submission Guidelines
1. Please upload your codebase and APK (or IPA) build zipped to the OneDrive folder.
2. Include setup instructions in your README.md
3. Prepare to demonstrate your app in an iOS/Android emulator

## Evaluation Criteria
- Code quality and organization
- Implementation of required features
- UI/UX design choices
- State management implementation
- Testing approach
- Documentation quality


We'll review your code and discuss your implementation during a technical interview.
