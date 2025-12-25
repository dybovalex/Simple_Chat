# Simple Chat

A lightweight chat application built with Flask and SQLAlchemy.

## Features

- User management with unique nicknames
- Individual chat rooms for each user
- Message persistence with SQLite database
- Clean, responsive UI with Bootstrap 5
- Flash messages for user feedback

## Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy, Flask-WTF
- **Frontend:** Jinja2 templates, Bootstrap 5 (via Flask-Bootstrap)
- **Database:** SQLite

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

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

3. Run the application:

   ```bash
   # Using uv
   uv run python main.py

   # Or directly
   python main.py
   ```

4. Open your browser and navigate to `http://127.0.0.1:5000/`

## Usage

- Visit the home page to see all users
- Click "Add New User" to create a new user with a unique nickname
- Click on a user card to open their chat room
- Messages are persisted in the SQLite database

## Project Structure

```
simple-chat/
├── main.py                  # Application entry point
├── pyproject.toml           # Project configuration and dependencies
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration settings
│   ├── forms.py             # WTForms definitions
│   ├── models.py            # SQLAlchemy models (User, Message)
│   └── routes.py            # Route handlers
├── static/
│   ├── css/
│   │   ├── style_input_form.css
│   │   └── style_user_card.css
│   └── js/
│       └── chat.js
├── templates/
│   ├── base.html            # Base template
│   ├── index.html           # Home page (user list)
│   ├── chat.html            # Chat room page
│   └── components/
│       ├── card.html
│       ├── input-field.html
│       ├── navbar.html
│       └── user-card.html
└── instance/                # SQLite database (auto-generated)
```

## License

MIT License
