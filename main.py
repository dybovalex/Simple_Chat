from enum import Enum

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


class MessageType(Enum):
    user_message = "user_message"
    response = "response"


app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=True)
    message = db.Column(db.String(500), nullable=False)
    message_type = db.Column(db.Enum(MessageType), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, user: str | None = None, message: str = "", **kwargs):
        super().__init__(**kwargs)
        self.user = user
        self.message = message
        return f"<Message {self.id} - {self.user} - {self.message} - {self.created_at}>"


@app.route("/<user>", methods=["GET", "POST"])
def index(user):
    if request.method == "POST":
        new_message = Message(user=user, message=request.form["user_message"], message_type=MessageType.user_message)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for("index", user=user))

    messages = Message.query.filter_by(user=user).order_by(Message.created_at.asc()).all()
    return render_template("index.html", user=user, messages=messages)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
