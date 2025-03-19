# NoteGenius-AI

## Overview
NoteGenius is a CRUD application for managing notes, but with a unique twist: whenever a note is created or updated, an AI-powered summarization of the content is generated. The project also includes various analytics endpoints for deeper insights into note content.

## Features
- **CRUD Operations**: Create, read, update, and delete notes.
- **AI-Powered Summarization**: Notes are automatically summarized upon creation or update.
- **Analytics Endpoints**:
  - Get common words used across all notes.
  - Get the average length of notes.
  - Get the total word count of all notes.
  - Retrieve the longest and shortest notes.
- **Testing**: Includes both unit and integration tests.

## Installation & Usage
The project is containerized and can be easily set up using Docker.

### Installing
```sh
git clone https://github.com/denis-rizun/NoteGenius-AI.git
```

### Running the Application

```sh
docker-compose up --build
```

### Running Tests
```sh
docker-compose run --rm web pytest
```
or
```sh
docker-compose run test
```

## Technologies Used
- **FastAPI** (for the backend)
- **PostgreSQL** (for data storage)
- **Docker & Docker Compose** (for containerization)
- **Pytest** (for unit and integration tests)

## License
This project is created for educational purposes only and is distributed without warranty of any kind

# Implementation Decisions
### Layered Architecture
I chose a layered architecture to maintain separation of concerns and ensure that different aspects of the application—such as data access, business logic, and API handling—are modular and independently scalable. This approach enhances maintainability and testability by preventing unnecessary dependencies between layers.

### Asynchronous Code
The application is built with asynchronous processing to maximize performance and responsiveness. This is particularly beneficial in scenarios where multiple operations—such as database queries or external API calls—might otherwise block execution. Instead of waiting for a response from, say, an AI API request, the system can continue handling other tasks, ensuring a smoother user experience.

### Database Trigger Instead of Additional Queries
Rather than performing additional queries on a secondary table (note_version), I opted to use a database trigger to automatically handle versioning upon insert and update operations. Since SQLAlchemy does not provide robust support for asynchronous triggers, I had to slightly compromise on the design by ensuring that the trigger executes after add and update operations on the note table. This keeps the system efficient while avoiding unnecessary overhead from multiple queries.

### Session Management in a Single File
The database session setup and its dependency injection are managed within a single file. This decision was made because the application does not anticipate additional dependencies that would require more complex session management. Keeping it centralized simplifies configuration and maintenance.

### Error Handling for a Better API Experience
To improve usability, the API includes error handling that captures and properly processes exceptions. This ensures that users receive meaningful error messages rather than generic server errors, enhancing the overall developer experience when integrating with the API.

### AI API Request Handling
For AI-powered operations—such as summarization—I chose not to introduce Celery since there was only a single AI API request per operation. While FastAPI’s BackgroundTask could have been an alternative, it does not guarantee task execution. Given that AI processing takes around 3 to 5 seconds and is crucial for both note creation and modification, I decided to handle it asynchronously within the request lifecycle. This ensures reliability without unnecessary complexity.

### Analytics with NumPy Instead of Pandas
For analytics-related endpoints, I opted for NumPy instead of Pandas. Since the use case primarily involves numerical calculations rather than structured tabular data manipulation, NumPy provides a lightweight and efficient solution. I also chose not to use NLTK for text analysis due to its overhead; for the required operations, a simpler approach was more appropriate.

### Testing Strategy
Tests are structured with a conftest.py file inside tests/unit_tests or tests/integration_tests, allowing for granular control over test execution. By setting specific tests to True, unnecessary tests can be skipped, improving efficiency. Additionally, due to limitations in ChatGPT’s free-tier for handling large-scale summarization tasks, I recommend executing test cases separately rather than running them all simultaneously to ensure optimal performance.
