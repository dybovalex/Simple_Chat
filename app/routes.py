from flask import Blueprint, render_template, request, redirect, url_for

from app import db
from app.models import Message, MessageType

main = Blueprint("main", __name__)


@main.route("/<user>", methods=["GET", "POST"])
def index(user):
    if request.method == "POST":
        new_message = Message(
            user=user,
            message=request.form["user_msg"],
            message_type=MessageType.user_message,
        )
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for("main.index", user=user))

    messages = (
        Message.query.filter_by(user=user).order_by(Message.created_at.asc()).all()
    )
    return render_template("index.html", user=user, messages=messages)
