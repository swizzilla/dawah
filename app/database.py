import os
import sqlite3
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import inspect

from app.config import DATABASE_URL, BASE_DIR

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Account(Base):
    """YouTube account for uploading videos"""
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)  # "MusicChannel", "GamingChannel"
    credentials_path = Column(String(500), nullable=True)  # Path to OAuth token pickle
    created_at = Column(DateTime, default=datetime.utcnow)

    conversations = relationship("Conversation", back_populates="account")


class Conversation(Base):
    """WhatsApp conversation state for upload flow"""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(50), nullable=False, index=True)

    # State machine
    state = Column(String(50), default="idle")
    # States: idle, awaiting_link, awaiting_audio, awaiting_account, awaiting_title,
    #         awaiting_description, awaiting_thumbnail, awaiting_privacy, processing

    # Upload data (collected during conversation)
    youtube_url = Column(String(500), nullable=True)
    audio_path = Column(String(500), nullable=True)  # Path to uploaded audio file
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    title = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    thumbnail_path = Column(String(500), nullable=True)
    privacy = Column(String(20), default="public")  # public, unlisted, private

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    account = relationship("Account", back_populates="conversations")


def migrate_database():
    """Add audio_path column if it doesn't exist"""
    # Connect directly to SQLite database to perform migration
    db_path = BASE_DIR / "yt_assistant.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if audio_path column exists
    cursor.execute("PRAGMA table_info(conversations)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'audio_path' not in columns:
        print("❌ audio_path column not found, adding it to conversations table...")
        cursor.execute("ALTER TABLE conversations ADD COLUMN audio_path TEXT")
        conn.commit()
        print("✅ audio_path column added successfully")
    else:
        print("✅ audio_path column already exists")
    
    conn.close()


def init_db():
    """Create all tables and run migrations"""
    # First create all tables
    Base.metadata.create_all(bind=engine)
    
    # Then run migrations
    migrate_database()


def get_db():
    """Dependency for FastAPI routes"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()