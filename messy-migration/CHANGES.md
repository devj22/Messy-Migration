# CHANGES.md

## Major Issues Identified
- SQL injection vulnerabilities due to string interpolation in SQL queries
- Plaintext password storage and authentication
- No input validation or error handling
- All logic in a single file, no separation of concerns
- No use of Flask best practices (Blueprints, jsonify, status codes)
- No tests

## Changes Made
- Refactored codebase into modular structure: separated routes, database logic, and app creation
- All SQL queries now use parameterized queries to prevent SQL injection
- Passwords are hashed using passlib (pbkdf2_sha256) before storage and checked securely on login
- Added input validation and proper error handling for all endpoints
- Used Flask Blueprints for route organization
- Used Flask's jsonify and proper HTTP status codes for all responses
- Added environment variable support for database path
- Updated requirements.txt to include passlib
- Updated init_db.py to hash sample passwords

## Assumptions / Trade-offs
- Assumed email is not unique in schema, so duplicate user creation returns 409 but does not enforce unique constraint
- Did not add user registration or email verification (not in scope)
- Did not add logging or advanced error handling to keep code simple
- Did not add full test suite due to time constraints

## What I'd Do With More Time
- Add unit and integration tests for all endpoints
- Enforce unique email constraint in the database
- Add logging and monitoring
- Use Flask-Migrate or Alembic for DB migrations
- Add configuration management for different environments
- Improve input validation (e.g., email format, password strength)
- Add rate limiting and further security hardening

## AI Usage
- Used ChatGPT for code review, refactor suggestions, and some code generation (especially for modularization and security improvements). All code was reviewed and tested manually. 