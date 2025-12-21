# Simple Chat

A lightweight chat application built with Flask and SQLAlchemy.

## Features

- User-based chat rooms (accessed via URL path)
- Message persistence with SQLite database
- Clean, responsive UI with Bootstrap 5

## Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy
- **Frontend:** Jinja2 templates, Bootstrap 5
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
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   # Using uv
   uv run python main.py

   # Or directly
   python main.py
   ```

4. Open your browser and navigate to `http://127.0.0.1:5000/<username>` (replace `<username>` with any name to start chatting).

## Usage

- Access the chat by visiting `http://127.0.0.1:5000/your_name`
- Each unique URL path creates a separate chat room for that user
- Messages are persisted in the SQLite database

## Project Structure

```
simple-chat/
├── main.py              # Flask application entry point
├── pyproject.toml       # Project configuration and dependencies
├── static/
│   └── css/
│       └── style_input_form.css
├── templates/
│   ├── base.html        # Base template
│   ├── index.html       # Main chat page
│   └── components/
│       ├── card.html
│       └── input-field.html
└── instance/            # SQLite database (auto-generated)
```

## License

MIT License
