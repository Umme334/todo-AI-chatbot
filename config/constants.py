"""Constants for Todo AI Chatbot."""

# Task statuses
TASK_STATUS_PENDING = "pending"
TASK_STATUS_COMPLETED = "completed"
TASK_STATUS_ARCHIVED = "archived"

# Task priorities
TASK_PRIORITY_LOW = -1
TASK_PRIORITY_NORMAL = 0
TASK_PRIORITY_HIGH = 1

# Default pagination
DEFAULT_LIMIT = 10
DEFAULT_OFFSET = 0

# MCP Tool names
MCP_TOOL_ADD_TASK = "add_task"
MCP_TOOL_LIST_TASKS = "list_tasks"
MCP_TOOL_COMPLETE_TASK = "complete_task"
MCP_TOOL_UPDATE_TASK = "update_task"
MCP_TOOL_DELETE_TASK = "delete_task"

# Database table names
TABLE_USERS = "users"
TABLE_TASKS = "tasks"
TABLE_THREADS = "threads"
TABLE_MESSAGES = "messages"

# Error messages
ERROR_INVALID_CREDENTIALS = "Invalid credentials"
ERROR_USER_NOT_FOUND = "User not found"
ERROR_TASK_NOT_FOUND = "Task not found"
ERROR_UNAUTHORIZED = "Unauthorized"
ERROR_FORBIDDEN = "Forbidden"