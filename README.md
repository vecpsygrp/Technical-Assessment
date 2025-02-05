# Mobile Developer Technical Assignment

## Overview
Build a mobile quiz application that demonstrates your ability to implement state management, local storage, and UI development following mobile best practices. While React Native is our preferred framework, you're welcome to use any technology stack that you believe will allow you to create the best possible application.

## API Information
The quiz API is deployed and available at:
https://vpg-tech-assessment-agg9exckazhhawdr.eastus-01.azurewebsites.net

### API Testing with Postman
To help you test and understand the API endpoints, we've provided a Postman collection that includes all endpoints with example requests. You can find it in the `postman_collection.json` file.

To use the collection:
1. Download and install [Postman](https://www.postman.com/downloads/)
2. Import the `postman_collection.json` file into Postman
3. The collection includes:
   - Pre-configured requests for all endpoints
   - Example request bodies
   - Automated tests for response validation
   - Environment variables for base URL and auth token

The collection will automatically save your authentication token after you get one, making it easier to test subsequent endpoints.

## Authentication
The API uses token-based authentication. Before making any requests, you need to obtain an authentication token. You can use any mock username of your choice (e.g., "test_user", "john_doe", etc.) - there's no need for real credentials.

1. Get an authentication token:
```http
POST /api/get_auth_token
Content-Type: application/json

{
    "user_name": "test_user"  // Can be any username you choose
}
```

Response:
```json
{
    "token": "generated-uuid-token",
    "user_name": "test_user"
}
```

2. Use this token in all subsequent API requests.

### API Endpoints

- `POST /api/get_auth_token` - Generate authentication token
- `GET /api/questions/<token>` - Returns the list of quiz questions
- `POST /api/responses/<token>` - Save an answer
  ```json
  {
    "question_index": 0,      
    "response": "Without any difficulty" 
  }
  ``` 
- `GET /api/responses/<token>/<user_name>` - Get all responses for a user
- `GET /api/progress/<token>` - Get survey progress for the authenticated user
- `GET /api/health` - Health check endpoint

### API Response Examples

#### Get Progress Response
```json
{
    "total_questions": 10,
    "answered_questions": 3,
    "progress": 0.3
}
```

#### Error Responses
Invalid token:
```json
{
    "error": "Invalid token"
}
```

Missing fields:
```json
{
    "error": "Missing required fields"
}
```

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

## Your Task: Mobile Quiz App

### Required Screens

1. Welcome/Start Screen
   - Clean, welcoming interface
   - Username input field
   - Start button (disabled until username is entered)
   - Handle new and returning users appropriately

2. Question Screen
   - Display one question at a time
   - Show question text prominently
   - Present multiple-choice answers in a clear, tappable format
   - Next/Previous navigation buttons
   - Next button should be disabled until an answer is selected
   - Previous button should allow reviewing/modifying previous answers
   - Progress indicator showing "Question X of Y" (e.g., "Question 3/10")
   - Consider adding animations for question transitions

3. Completion Screen
   - Congratulatory/Submission success message
   - Summary of all questions and the user's responses
   - Option to review/modify any answers
   - Clear presentation of survey completion status
   - Consider adding a visual representation of responses

### Core Features

1. Create a mobile app that implements a step-by-step health survey:
   - Handle user authentication using the provided API
   - Save responses after each question
   - Maintain survey progress
   - Support offline functionality (optional)
   - Implement smooth navigation between screens

2. Data Management:
   - Fetch and cache survey questions
   - Store user responses locally
   - Sync responses with the API
   - Track survey progress
   - Handle error cases gracefully

### Technical Requirements
- Use your preferred mobile development framework (React Native recommended but not required)
- Implement appropriate state management for your chosen framework
- Use local storage for data persistence (e.g., AsyncStorage for React Native)
- Demonstrate proper data fetching patterns (loading states, error handling)
- Follow mobile development best practices for your chosen framework

### UI/UX Requirements
- Clean, intuitive interface for each question screen
- Clear visual hierarchy for question text and answer options
- Smooth transitions between questions
- Visible progress indicator (e.g., "3/10")
- Disabled "Next" button until an answer is selected
- Clear completion summary showing all questions and selected answers

### Bonus Points (Completely Optional)
- Enhanced Features:
  - Ability to review and modify previous answers
  - Save partial progress and resume later
  - Offline support with data sync
  - Creative UI/UX improvements
- Polish:
  - Screen transition animations
  - Creative results visualization
  - Performance optimizations
- Code Quality:
  - Unit tests
  - Code documentation

## Submission Guidelines
1. Upload your codebase and compiled app (APK for Android or IPA for iOS) zipped to the OneDrive folder
2. Include in your README.md:
   - Setup instructions for running your project
   - Brief explanation of your technology choices
   - Any additional features or improvements you've implemented
3. Prepare to demonstrate your app in an appropriate emulator/simulator

## Evaluation Criteria
- Code quality and organization
- Implementation of required features
- UI/UX design choices
- State management implementation
- Testing approach
- Documentation quality
- Rationale for technical choices

We'll review your code and discuss your implementation during a technical interview.
