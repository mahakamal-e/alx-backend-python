# Messaging API Project

## Overview

This is a simple messaging API built using Django and Django REST Framework. It allows users to create conversations and send messages within those conversations. The project is structured to support nested routing using `drf-nested-routers`, which enables endpoints like:


## Features

- Create a new conversation.
- View a list of all conversations.
- Send messages to a specific conversation.
- View all messages under a specific conversation.

## Technologies Used

- Python
- Django
- Django REST Framework
- drf-nested-routers

## Installation

1. Clone the repository:
   ```bash
   git clone 
   cd messaging_app

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install dependencies
   ```bash
   pip install -r requirements.txt

4. Run migrations
   ```bash
   python manage.py migrate

5. Start the development server
   ```bash
   python manage.py runserver

## API Endpoints

### Method | Endpoint | Description
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /conversations/ | List all conversations |
| POST   | /conversations/ | Create a new conversation |
| GET    | /conversations/{conversation_id}/messages/ | List all messages in a conversation |
| POST   | /conversations/{conversation_id}/messages/ | Send a new message |

---

## Example Requests

### Creating a Conversation

**POST** `/conversations/`

```json
{
  "title": "Chat with Ali"
}