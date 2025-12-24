from enum import Enum
from datetime import datetime
from app import db


class MessageType(Enum):
    user_message = "user_message"
    response = "response"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationship: one user can have many messages
    messages = db.relationship("Message", backref="author", lazy=True)

    def __init__(self, nickname: str) -> None:
        self.nickname = nickname

    def __repr__(self):
        return f"<User {self.id} - {self.nickname}>"


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    message = db.Column(db.String(500), nullable=False)
    message_type = db.Column(db.Enum(MessageType), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(
        self,
        message: str,
        user_id: int | None = None,
        message_type: MessageType | None = None,
    ) -> None:
        self.message = message
        self.user_id = user_id
        self.message_type = message_type

    def __repr__(self):
        return f"<Message {self.id} - {self.user_id} - {self.message[:20]}>"
