# API Documentation
## Overview
This API serves as the backend for a chatbot application. It provides endpoints for user authentication, user registration, chatbot interactions, and user profile management. The backend is built using Flask and SQLite for data storage.

# Endpoints
  - `Home`
      - Route: /
      - Method: GET
      - Description: A simple route to verify if the Flask application is working.

  - `Sign In`
      - Route: /signin
      - Method: POST
      - Description: Authenticate and log in a user.
      - Request Data Format: JSON with 'email' and 'password' fields.
    
  - `Register`
      - Route: /register
      - Method: POST
      - Description: Create a new user account.
      - Request Data Format: JSON with 'name', 'email', and 'password' fields.
    
  - `Chatbot`
      - Route: /chatbot
      - Method: PUT
      - Description: Update a user's chat data.
      - Request Data Format: JSON with 'id' and 'chat' fields to update the user's chat data.
    
  - `User Profile`
      - Route: /profile/<user_id>
      - Method: GET
      - Description: Fetch a user's profile by user_id.

## Data Model
The backend uses a SQLite database with the following table structure:
  - users
    - `id (UUID)`: User's unique identifier.
    - `name (VARCHAR)`: User's name.
    - `email (VARCHAR)`: User's email.
    - `password (VARCHAR)`: User's hashed password.
    - `chats (VARCHAR)`: User's chat data.
    - `joined (TIMESTAMP)`: User's registration date and time.

## Security
User passwords are securely hashed using bcrypt for storage, providing a high level of security. User authentication is performed by checking the hashed password.

## Usage
  - To run the Flask application, use python app.py.
  - The application is available at http://localhost:5000.

## Deployment
This project was particularly deployed on render and can be found at `https://swiftchat-server.onrender.com`
