# Simple Chat

A lightweight chat application built with Flask and FastAPI, featuring AI-powered responses via OpenAI.

> 🎓 **This is a learning project** — built to explore Flask, FastAPI, and OpenAI API integration.

## Features

- User management with unique nicknames
- Individual chat rooms for each user
- **AI-powered responses** using OpenAI GPT-4o-mini
- Message context awareness (uses recent conversation history)
- Message persistence with SQLite database
- Clean, responsive UI with Bootstrap 5
- Flash messages for user feedback

## Tech Stack

- **Frontend:** Flask, Flask-SQLAlchemy, Flask-WTF, Jinja2 templates, Bootstrap 5
- **AI Service:** FastAPI, Uvicorn, OpenAI API
- **Database:** SQLite (shared between services)
- **HTTP Client:** httpx (for inter-service communication)

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- OpenAI API key

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/YOUR_USERNAME/simple-chat.git
   cd simple-chat
   ```

2. Install dependencies:

   ```bash
   # Using uv (recommended)
   uv sync

   # Or using pip
   pip install -e .
   ```

3. Create a `.env` file in the project root with your OpenAI API key:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Running the Application

You need to run **two services** for full functionality:

### 1. Start the AI Service (FastAPI)

```bash
# Using uv
uv run uvicorn ai_service.main_ai:app --reload

# Or directly
uvicorn ai_service.main_ai:app --reload
```

The AI service runs on `http://localhost:8000`

### 2. Start the Web Application (Flask)

In a separate terminal:

```bash
# Using uv
uv run python main.py

# Or directly
python main.py
```

The web app runs on `http://localhost:5000`

### 3. Open your browser

Navigate to `http://127.0.0.1:5000/`

## Usage

1. Visit the home page to see all users
2. Click "Add New User" to create a new user with a unique nickname
3. Click on a user card to open their chat room
4. Type a message and the AI will respond automatically
5. Messages are persisted in the SQLite database

> **Note:** If the AI service is unavailable, your messages will still be saved, and you'll see a warning notification.

## Architecture

```
┌─────────────────┐     HTTP POST      ┌─────────────────┐
│   Flask App     │ ────────────────▶  │  FastAPI AI     │
│   (Port 5000)   │                    │  (Port 8000)    │
└────────┬────────┘                    └────────┬────────┘
         │                                      │
         │                                      │
         ▼                                      ▼
┌─────────────────────────────────────────────────────────┐
│                    SQLite Database                       │
│                   (instance/chat.db)                     │
└─────────────────────────────────────────────────────────┘
                                                │
                                                ▼
                                    ┌─────────────────┐
                                    │   OpenAI API    │
                                    │  (GPT-4o-mini)  │
                                    └─────────────────┘
```

## Project Structure

```
simple-chat/
├── main.py                      # Flask application entry point
├── pyproject.toml               # Project configuration and dependencies
├── .env                         # Environment variables (create this)
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Flask configuration
│   ├── forms.py                 # WTForms definitions
│   ├── models.py                # SQLAlchemy models (User, Message)
│   ├── routes.py                # Flask route handlers
│   └── shared/
│       └── config.py            # Shared configuration (DB path, API keys)
├── ai_service/
│   └── main_ai.py               # FastAPI AI service with OpenAI integration
├── static/
│   ├── css/
│   │   ├── style_input_form.css
│   │   └── style_user_card.css
│   └── js/
│       └── chat.js
├── templates/
│   ├── base.html                # Base template
│   ├── index.html               # Home page (user list)
│   ├── chat.html                # Chat room page
│   └── components/
│       ├── card.html
│       ├── input-field.html
│       ├── navbar.html
│       └── user-card.html
└── instance/                    # SQLite database (auto-generated)
    └── chat.db
```

## API Endpoints

### Flask App (Port 5000)

| Method   | Endpoint           | Description              |
| -------- | ------------------ | ------------------------ |
| GET      | `/`                | Home page with user list |
| GET/POST | `/chat/<nickname>` | Chat room for a user     |
| POST     | `/create-user`     | Create a new user        |

### FastAPI AI Service (Port 8000)

| Method | Endpoint          | Description                        |
| ------ | ----------------- | ---------------------------------- |
| GET    | `/`               | Health check                       |
| POST   | `/generate-reply` | Generate AI response for a message |

## Configuration

Environment variables (set in `.env` file):

| Variable         | Description         | Required |
| ---------------- | ------------------- | -------- |
| `OPENAI_API_KEY` | Your OpenAI API key | Yes      |

Default settings in `app/shared/config.py`:

- **Timezone:** Europe/Vienna
- **Database:** `instance/chat.db`
- **AI Model:** GPT-4o-mini

## License

MIT License
