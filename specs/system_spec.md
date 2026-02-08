# Phase-3 Todo AI Chatbot - System Specification

## 1. System Overview

The Todo AI Chatbot is an intelligent task management system that enables users to manage their todos through natural language interactions. The system leverages OpenAI's Agent technology to interpret user commands and executes corresponding actions via MCP tools. Built with a stateless FastAPI backend, it follows modern architectural principles with persistent storage in Neon Serverless PostgreSQL and SQLModel as the ORM.

### Core Capabilities
- Natural language processing for todo management
- Intelligent task interpretation and execution
- Real-time chat interface with OpenAI ChatKit
- Secure authentication via Better Auth
- Scalable, stateless architecture

## 2. Architecture Diagram Explanation

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │◄──►│   FastAPI        │◄──►│   MCP Tools     │
│  (OpenAI ChatKit)│    │   Backend        │    │   (DB Ops)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │                          │
                              ▼                          ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │ Better Auth      │    │  Neon PostgreSQL│
                       │ (Authentication) │    │  (SQLModel)     │
                       └──────────────────┘    └─────────────────┘
```

### Component Roles
- **Frontend**: Real-time chat interface using OpenAI ChatKit
- **FastAPI Backend**: Stateless API gateway and agent orchestration
- **Better Auth**: Authentication and user session management
- **MCP Tools**: Database operation handlers (stateless)
- **Neon PostgreSQL**: Persistent storage with SQLModel ORM

## 3. API Contracts

### 3.1 Chat Endpoint
```
POST /api/chat
Authorization: Bearer {token}

Request Body:
{
  "messages": [
    {
      "role": "user",
      "content": "Add a new task to buy groceries"
    }
  ],
  "thread_id": "optional_thread_id"
}

Response:
{
  "response": "Successfully added task: Buy groceries",
  "actions_taken": [
    {
      "action": "add_task",
      "result": "task_created",
      "task_id": 123
    }
  ]
}
```

### 3.2 Thread Management Endpoints
```
GET /api/threads/{thread_id}
POST /api/threads
DELETE /api/threads/{thread_id}
```

## 4. Database Schema

### 4.1 User Table
```sql
users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### 4.2 Task Table
```sql
tasks (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  title VARCHAR(500) NOT NULL,
  description TEXT,
  status VARCHAR(20) DEFAULT 'pending', -- pending, completed, archived
  priority INTEGER DEFAULT 0, -- 0=normal, 1=high, -1=low
  due_date TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### 4.3 Thread Table
```sql
threads (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  title VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### 4.4 Message Table
```sql
messages (
  id UUID PRIMARY KEY,
  thread_id UUID REFERENCES threads(id),
  role VARCHAR(20) NOT NULL, -- user, assistant
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## 5. MCP Tools Specification

### 5.1 add_task
**Purpose**: Creates a new task for the authenticated user
**Parameters**:
- `title`: String (required) - Task title
- `description`: String (optional) - Task description
- `due_date`: String (optional) - Due date in ISO format
- `priority`: Integer (optional) - Priority level (-1, 0, 1)

**Return**: Task object with ID and confirmation

### 5.2 list_tasks
**Purpose**: Retrieves tasks for the authenticated user
**Parameters**:
- `status_filter`: String (optional) - Filter by status ('pending', 'completed', 'all')
- `limit`: Integer (optional) - Number of tasks to return (default: 10)
- `offset`: Integer (optional) - Offset for pagination

**Return**: Array of task objects

### 5.3 complete_task
**Purpose**: Marks a task as completed
**Parameters**:
- `task_id`: UUID (required) - ID of the task to complete

**Return**: Updated task object

### 5.4 update_task
**Purpose**: Updates task properties
**Parameters**:
- `task_id`: UUID (required) - ID of the task to update
- `title`: String (optional) - New title
- `description`: String (optional) - New description
- `due_date`: String (optional) - New due date
- `priority`: Integer (optional) - New priority

**Return**: Updated task object

### 5.5 delete_task
**Purpose**: Permanently deletes a task
**Parameters**:
- `task_id`: UUID (required) - ID of the task to delete

**Return**: Confirmation of deletion

## 6. Agent Behavior Rules

### 6.1 Natural Language Processing
- Interpret task creation requests: "Add task", "Create", "Remember to"
- Recognize due dates: "by tomorrow", "next week", "in 3 days"
- Identify priorities: "urgent", "important", "asap" → high priority
- Parse complex requests: "Remind me to buy milk and eggs by Friday"

### 6.2 Context Awareness
- Maintain conversation context within a thread
- Recognize pronouns: "it", "that", "the task" (when referring to last mentioned)
- Handle follow-up requests: "Change its due date to Monday"
- Preserve user intent across multiple messages

### 6.3 Validation Logic
- Validate date formats and convert to standard format
- Confirm destructive actions (deletion) before executing
- Provide helpful suggestions when requests are ambiguous

## 7. Error Handling Rules

### 7.1 Authentication Errors
- Return 401 Unauthorized for invalid tokens
- Provide clear error message for expired sessions

### 7.2 Validation Errors
- Return 422 Unprocessable Entity for invalid parameters
- Include specific field-level error messages

### 7.3 Business Logic Errors
- Return 404 Not Found for non-existent resources
- Return 403 Forbidden for unauthorized access attempts

### 7.4 System Errors
- Return 500 Internal Server Error for unexpected issues
- Log errors with correlation IDs for debugging
- Never expose sensitive system information to clients

## 8. Stateless Request Lifecycle

1. **Request Received**: FastAPI receives authenticated request
2. **User Validation**: Better Auth validates JWT token
3. **Agent Invocation**: OpenAI Agent processes user message
4. **Tool Selection**: Agent determines appropriate MCP tools
5. **Tool Execution**: MCP tools execute database operations
6. **Response Assembly**: Agent composes response from tool results
7. **Response Sent**: JSON response returned to client
8. **State Cleanup**: No server-side state retained between requests

## 9. Folder Structure

```
todo-ai-chatbot/
├── api/                    # API endpoints and route definitions
│   ├── __init__.py
│   ├── chat.py            # Chat endpoints
│   ├── threads.py         # Thread management
│   └── auth.py            # Authentication routes
├── models/                 # SQLModel database models
│   ├── __init__.py
│   ├── user.py            # User model
│   ├── task.py            # Task model
│   ├── thread.py          # Thread model
│   └── message.py         # Message model
├── tools/                  # MCP tools for database operations
│   ├── __init__.py
│   ├── task_tools.py      # Task-related tools
│   └── utils.py           # Tool utilities
├── agents/                 # OpenAI Agent implementations
│   ├── __init__.py
│   ├── chat_agent.py      # Main chat agent
│   └── orchestrator.py    # Agent orchestrator
├── database/               # Database connection and setup
│   ├── __init__.py
│   ├── connection.py      # Connection pooling
│   └── migrations.py      # Migration scripts
├── schemas/                # Pydantic schemas for validation
│   ├── __init__.py
│   ├── user.py            # User schemas
│   ├── task.py            # Task schemas
│   └── chat.py            # Chat schemas
├── config/                 # Configuration files
│   ├── __init__.py
│   ├── settings.py        # Settings management
│   └── constants.py       # App constants
├── frontend/               # Frontend files (if not using external)
│   ├── index.html
│   ├── css/
│   └── js/
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_chat.py       # Chat functionality tests
│   ├── test_auth.py       # Authentication tests
│   └── conftest.py        # Test fixtures
├── alembic/                # Database migration configs
├── Dockerfile             # Container definition
├── docker-compose.yml     # Multi-container setup
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore patterns
├── README.md              # Project documentation
├── main.py                # Application entry point
└── pyproject.toml         # Poetry/pyproject configuration
```

## 10. Non-Functional Requirements

### 10.1 Performance
- Response time < 2 seconds for typical operations
- Support for 1000+ concurrent users
- 99.9% uptime SLA

### 10.2 Scalability
- Horizontal scaling capability
- Database connection pooling
- Stateless design for containerization

### 10.3 Security
- JWT-based authentication with short-lived tokens
- Input sanitization to prevent injection attacks
- Rate limiting to prevent abuse
- Secure transmission with HTTPS

### 10.4 Reliability
- Comprehensive error handling and logging
- Database transaction integrity
- Graceful degradation under load
- Automated backup procedures

### 10.5 Maintainability
- Clear separation of concerns
- Comprehensive logging and monitoring
- Well-documented APIs
- Automated testing coverage >80%