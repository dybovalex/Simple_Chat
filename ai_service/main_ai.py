from openai import OpenAI
from pydantic import BaseModel
from datetime import datetime, date
import pytz
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import sessionmaker, declarative_base
import enum
from fastapi import FastAPI
from app.shared.config import DATABASE_URI, OPENAI_API_KEY, TIMEZONE

app = FastAPI()

# Database setup
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


class MessageType(enum.Enum):
    user_message = "user_message"
    response = "response"


class Message(Base):
    __tablename__ = "message"  # Must match existing table name!

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    message = Column(String(500), nullable=False)
    message_type = Column(Enum(MessageType), nullable=True)
    created_at = Column(DateTime, default=datetime.now)


# Pydantic models for API
class GenerateReplyRequest(BaseModel):
    user_id: int
    user_message_text: str


class GenerateReplyResponse(BaseModel):
    assistant_response: str
    user_message_id: int
    response_message_id: int


@app.post("/generate-reply", response_model=GenerateReplyResponse)
def generate_reply(request: GenerateReplyRequest):
    db = SessionLocal()
    try:
        # Step 1: Save the user message to database
        user_message = Message(
            user_id=request.user_id,
            message=request.user_message_text,
            message_type=MessageType.user_message,
        )
        db.add(user_message)
        db.commit()
        db.refresh(user_message)  # Get the generated ID

        # Step 2: Get today's date in Vienna timezone
        vienna_tz = pytz.timezone(TIMEZONE)
        now_vienna = datetime.now(vienna_tz)
        today_start = now_vienna.replace(hour=0, minute=0, second=0, microsecond=0)

        # Step 3: Fetch up to 5 most recent messages from today for this user
        recent_messages = (
            db.query(Message)
            .filter(Message.user_id == request.user_id)
            .filter(Message.created_at >= today_start)
            .order_by(Message.created_at.desc())
            .limit(5)
            .all()
        )
        # Reverse to get chronological order (oldest first)
        recent_messages = list(reversed(recent_messages))

        # Step 4: Build OpenAI messages context
        openai_messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        for msg in recent_messages:
            role = (
                "user" if msg.message_type == MessageType.user_message else "assistant"
            )
            openai_messages.append({"role": role, "content": str(msg.message)})

        # Step 5: Call OpenAI API
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-3.5-turbo" for cheaper option
            messages=openai_messages,
        )
        assistant_response_text = completion.choices[0].message.content

        # Step 6: Save assistant response to database
        assistant_message = Message(
            user_id=request.user_id,
            message=assistant_response_text,
            message_type=MessageType.response,
        )
        db.add(assistant_message)
        db.commit()
        db.refresh(assistant_message)

        # Step 7: Return the response
        return GenerateReplyResponse(
            assistant_response=assistant_response_text,
            user_message_id=user_message.id,
            response_message_id=assistant_message.id,
        )
    finally:
        db.close()


@app.get("/")
def health_check():
    return {"status": "ok"}
