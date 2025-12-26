from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import User, Message, MessageType
from app.forms import AddUserForm
from sqlalchemy.exc import IntegrityError
import httpx


main = Blueprint("main", __name__)


def get_or_create_user(nickname):
    """Find existing user or create a new one."""
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        user = User(nickname=nickname)
        db.session.add(user)
        db.session.commit()
    return user


@main.route("/")
def home():
    """Home page - list all users."""
    users = User.query.order_by(User.created_at.desc()).all()
    form = AddUserForm()
    return render_template("index.html", users=users, form=form)


@main.route("/chat/<nickname>", methods=["GET", "POST"])
def chat(nickname):
    # Get or create the user
    user = get_or_create_user(nickname)

    if request.method == "POST":
        user_message_text = request.form["user_msg"]
        
        # Call FastAPI AI service
        try:
            with httpx.Client() as client:
                response = client.post(
                    "http://localhost:8000/generate-reply",
                    json={
                        "user_id": user.id,
                        "user_message_text": user_message_text
                    },
                    timeout=30.0  # 30 second timeout for OpenAI
                )
                response.raise_for_status()  # Raise exception for 4xx/5xx errors
        except httpx.RequestError as e:
            # FastAPI is down or network error
            # Save user message anyway, show error
            new_message = Message(
                user_id=user.id,
                message=user_message_text,
                message_type=MessageType.user_message,
            )
            db.session.add(new_message)
            db.session.commit()
            flash("AI service is unavailable. Your message was saved.", "warning")
        except httpx.HTTPStatusError as e:
            # FastAPI returned an error
            flash(f"AI service error: {e.response.status_code}", "danger")
        
        return redirect(url_for("main.chat", nickname=nickname))

    # Get all messages for this user
    messages = (
        Message.query.filter_by(user_id=user.id)
        .order_by(Message.created_at.asc())
        .all()
    )
    return render_template("chat.html", user=user, messages=messages)


@main.route("/create-user", methods=["POST"])
def create_user():
    form = AddUserForm()
    if form.validate_on_submit():
        nickname = (form.nickname.data or "").strip()
        try:
            user = User(nickname=nickname)
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("This nickname is already taken!", "danger")
        return redirect(url_for("main.home"))
    return redirect(url_for("main.home"))
