# API Documentation

This document describes the APIs available in the AiDemy platform. This is an enhanced version of the original Google Codelab project with additional API documentation and examples.

## Base URLs

- Development: `http://localhost:8080`
- Production: `https://[YOUR-PROJECT-ID].run.app`

## Authentication

All API endpoints require authentication using Google Cloud service accounts. Include the following header in your requests:

```
Authorization: Bearer [YOUR-TOKEN]
```

## Portal API

### Get Home Page
```http
GET /
```

Returns the main portal interface.

### Generate Quiz
```http
GET /generate_quiz
```

Generates a quiz with multiple difficulty levels.

**Response:**
```json
[
  {
    "question": "string",
    "options": ["string"],
    "answer": "string",
    "difficulty": "string"
  }
]
```

### Check Answers
```http
POST /check_answers
```

Evaluates student answers and provides feedback.

**Request Body:**
```json
{
  "quiz": [
    {
      "question": "string",
      "options": ["string"],
      "answer": "string"
    }
  ],
  "answers": ["string"]
}
```

**Response:**
```json
[
  {
    "question": "string",
    "user_answer": "string",
    "correct_answer": "string",
    "is_correct": boolean,
    "reasoning": "string"
  }
]
```

### Download Course Audio
```http
GET /download_course_audio/{week}
```

Downloads audio content for a specific week.

**Parameters:**
- `week` (integer): Week number

## Planner API

### Generate Teaching Plan
```http
POST /generate_plan
```

Generates a teaching plan based on curriculum requirements.

**Request Body:**
```json
{
  "subject": "string",
  "grade_level": "string",
  "duration": "string",
  "requirements": ["string"]
}
```

**Response:**
```json
{
  "plan_id": "string",
  "content": "string",
  "schedule": [
    {
      "week": integer,
      "topics": ["string"],
      "assignments": ["string"]
    }
  ]
}
```

## Courses API

### Get Course Content
```http
GET /courses/{course_id}
```

Retrieves course content and materials.

**Parameters:**
- `course_id` (string): Unique course identifier

**Response:**
```json
{
  "course_id": "string",
  "title": "string",
  "description": "string",
  "materials": [
    {
      "type": "string",
      "content": "string",
      "week": integer
    }
  ]
}
```

## Assignment API

### Create Assignment
```http
POST /assignments
```

Creates a new assignment.

**Request Body:**
```json
{
  "title": "string",
  "description": "string",
  "due_date": "string",
  "course_id": "string"
}
```

**Response:**
```json
{
  "assignment_id": "string",
  "status": "string",
  "created_at": "string"
}
```

### Submit Assignment
```http
POST /assignments/{assignment_id}/submit
```

Submits a student's assignment.

**Parameters:**
- `assignment_id` (string): Unique assignment identifier

**Request Body:**
```json
{
  "student_id": "string",
  "content": "string",
  "attachments": ["string"]
}
```

## Book Provider API

### Get Book Recommendations
```http
GET /books/recommendations
```

Gets personalized book recommendations.

**Query Parameters:**
- `subject` (string): Subject area
- `grade_level` (string): Grade level
- `reading_level` (string): Student's reading level

**Response:**
```json
{
  "recommendations": [
    {
      "book_id": "string",
      "title": "string",
      "author": "string",
      "description": "string",
      "reading_level": "string",
      "relevance_score": float
    }
  ]
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "string",
  "message": "string"
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing authentication token"
}
```

### 403 Forbidden
```json
{
  "error": "Forbidden",
  "message": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred"
}
```

## Rate Limiting

API requests are limited to:
- 100 requests per minute per IP
- 1000 requests per hour per user

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1623456789
```

## Versioning

The API is versioned through the URL path:
- Current version: `/v1`
- Example: `https://api.aidemy.com/v1/courses`

## Webhooks

The API supports webhooks for asynchronous events:

### Available Events
- `assignment.submitted`
- `quiz.completed`
- `course.progress`
- `teaching_plan.generated`

### Webhook Payload
```json
{
  "event": "string",
  "timestamp": "string",
  "data": {}
}
```

## SDK Examples

### Python
```python
from aidemy_sdk import AidemyClient

client = AidemyClient(api_key="your-api-key")

# Generate a quiz
quiz = client.generate_quiz()

# Submit answers
results = client.check_answers(quiz_id="123", answers=["A", "B", "C"])
```

### JavaScript
```javascript
const aidemy = require('aidemy-sdk');

const client = new AidemyClient({
  apiKey: 'your-api-key'
});

// Get book recommendations
const recommendations = await client.getBookRecommendations({
  subject: 'Mathematics',
  gradeLevel: 'High School'
});
``` 