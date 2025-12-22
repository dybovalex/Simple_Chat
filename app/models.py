from enum import Enum
from datetime import datetime
from app import db


class MessageType(Enum):
    user_message = "user_message"
    response = "response"


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
