from flask import Blueprint, render_template, request, redirect, url_for

from app import db
from app.models import User, Message, MessageType

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
    return render_template("index.html", users=users)


@main.route("/chat/<nickname>", methods=["GET", "POST"])
def chat(nickname):
    # Get or create the user
    user = get_or_create_user(nickname)

    if request.method == "POST":
        new_message = Message(
            user_id=user.id,
            message=request.form["user_msg"],
            message_type=MessageType.user_message,
        )
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for("main.chat", nickname=nickname))

    # Get all messages for this user
    messages = (
        Message.query.filter_by(user_id=user.id)
        .order_by(Message.created_at.asc())
        .all()
    )
    return render_template("chat.html", user=user, messages=messages)
